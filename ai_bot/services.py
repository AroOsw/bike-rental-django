import os
import logging
import glob
import random
from pathlib import Path
from django.conf import settings
from numpy.ma.core import count
from openai import OpenAI
from .models import KnowledgeBase
from core.models import BikeModel
from dotenv import load_dotenv
from pgvector.django import CosineDistance

load_dotenv()

logger = logging.getLogger(__name__)


class VectorService:
    """
    Service for handling vector embeddings and knowledge base synchronization
    """

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_name = "text-embedding-3-small"

    # Mock version for free
    # def get_embedding(self, text: str) -> list[float]:
    #     """Mock version - for tests without payments
    #     stimulating OpenAi answer returning 1536 random numbers"""
    #     print(f"--- MOCK: Generating fake vector for text: {text[:30]}... ---")
    #     return [random.uniform(-1, 1) for _ in range(1536)]

    # Basic version
    def get_embedding(self, text: str) ->list[float]:
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
        ).order_by("distance")[:3]

        if matches:
            context_list = []
            for match in matches:
                print(f"Found match in: {match.source} Distance: {match.distance}")
                context_list.append(match.content)
            return "\n\n---\n\n".join(context_list)

        return "No result"

    def ask_assistant(self, question):
        # 1. Get context from base
        context = self.get_context(question)

        messages=[
            {
              "role": "system",
              "content": f"You are a helpful assistant for a bike rental shop called WildWheel in Hua Hin, Thailand. "
              f"Answer the user's question using ONLY the following context:\n\n{context}"
            },
            {
            "role": "user",
            "content": question,
            }
        ]

        # 2. Prepare query for chat model
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content