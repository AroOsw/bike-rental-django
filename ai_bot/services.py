import os
import logging
from pathlib import Path
from django.conf import settings
from uuid import UUID
from openai import OpenAI
from .models import KnowledgeBase, ChatMessage, ChatSession
from core.models import BikeModel
from dotenv import load_dotenv
from pgvector.django import CosineDistance

load_dotenv()

logger = logging.getLogger(__name__)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class VectorService:
    """
    Service for handling vector embeddings and knowledge base synchronization
    """

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_name = "text-embedding-3-small"

    # Basic version
    def get_embedding(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            input=text,
            model=self.model_name
        )
        return response.data[0].embedding

    def update_knowledge(self, source, content):
        """Update or create knowledge base entry"""
        try:
            # 1. First download vector(list of numbers) for text
            vector = self.get_embedding(content)

            # 2. Save to the database
            KnowledgeBase.objects.update_or_create(
                source=source,
                defaults={
                    "content": content,
                    "embedding": vector,
                }
            )
            print(f"Success {source} synchronized")
            return True
        except Exception as e:
            print(f"Error {source}: {e}")
            return False

    def sync_static_knowledge(self):
        """Sync all markdown files from knowledge folder to the database"""
        path_to_knowledge = Path(settings.BASE_DIR) / 'ai_bot' / 'knowledge'
        count = 0

        if not path_to_knowledge.exists():
            print("This folder doesn't exist")
            return 0

        # target_file = path_to_knowledge / "ai-operational-knowledge.md"
        for file in path_to_knowledge.glob("*.md"):
            if file.exists():
                with open(file, "r", encoding="utf-8") as f:
                    content = f.read()

                    if content.strip():
                        self.update_knowledge(source=file.name, content=content)
                        count += 1
            else:
                print(f"File not found: {file.name}")
        return count

    def get_context(self, query_text):

        query_vector = self.get_embedding(query_text)

        matches = KnowledgeBase.objects.annotate(
            distance=CosineDistance("embedding", query_vector)
        ).order_by("distance")[:10]

        if matches:
            context_list = []
            for match in matches:
                print(f"Found match in: {match.source} Distance: {match.distance}")
                context_list.append(match.content)
            return "\n\n---\n\n".join(context_list)

        return "No result"

    def ask_assistant(self, all_messages: list[dict]):

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=all_messages,
            temperature=0.3,
        )
        return response


class ChatService:
    def __init__(self):
        self.vector_service = VectorService()

    def get_chat_response(self, session_id: UUID, user_message: str) -> str:

        try:
            session = ChatSession.objects.get(id=session_id)
            customer_message = ChatMessage.objects.create(
                session=session,
                content=user_message,
                role="user",
            )
            context = self.vector_service.get_context(user_message)
            chat_history = ChatMessage.objects.filter(session=session).order_by("timestamp")
            messages_to_send = [
                {
                    "role": "system",
                    "content": f"You are a helpful assistant for a bike rental shop called WildWheel in Hua Hin, Thailand. "
                               f"Answer the user's question using ONLY the following context, and chat history"
                               "If the answer is not in the context, inform the user that we don't have that specific"
                               "service or information, but always try to suggest the closest alternative available "
                               "in our shop (e.g., if someone asks for a helicopter, tell them we only rent bikes)."

                               "Be helpful and conversational, but never make up specific prices, distances, "
                               "or rules that are not in the context."

                               "If the user asks about something completely unrelated to bikes, tourism in Hua Hin,"
                               " or our shop, then and only then use the fallback: 'I'm sorry, "
                               "but I don't have information on this topic...'"
                               f"\n\n{context}"
                },
            ]
            for message in chat_history:
                messages_to_send.append({"role": message.role, "content": message.content})

            ask_assistant = self.vector_service.ask_assistant(messages_to_send)
            ai_answer = ChatMessage.objects.create(
                session=session,
                content=ask_assistant.choices[0].message.content,
                role="assistant",
                tokens_used=ask_assistant.usage.total_tokens
            )
            return ask_assistant.choices[0].message.content


        except ChatSession.DoesNotExist:
            raise ValueError("Session not found", None)
