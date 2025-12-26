import pytest
from unittest.mock import patch, MagicMock
from ai_bot.services import VectorService, ChatService
from ai_bot.models import ChatMessage

@pytest.mark.django_db
def test_get_chat_response_saves_to_db(chat_session, knowledge_base):
    user_msg = "What are opening hours?"
    sys_ctx = "Some of system data"

    with patch("ai_bot.services.OpenAI") as mock_openai_class:
        mock_client = mock_openai_class.return_value

        mock_client.embeddings.create.return_value = MagicMock(
            data=[MagicMock(embedding=[0.1] * 1536)]
        )

        mock_answer = "From 8am to 6pm."
        mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=mock_answer))],
            usage=MagicMock(total_tokens=50)
        )

        service = ChatService()
        response = service.get_chat_response(chat_session.id, user_msg, sys_ctx)

        print(f"response:{response} mock_answer:{mock_answer}")
        assert response == mock_answer
        assert ChatMessage.objects.filter(session=chat_session).count() == 2

        last_msg = ChatMessage.objects.filter(role="assistant").last()
        assert last_msg.content == mock_answer
        assert last_msg.tokens_used == 50

@pytest.mark.django_db
def test_update_knowledge_in_database():

    with patch("ai_bot.services.OpenAI") as mock_openai_class:

        mock_client = mock_openai_class.return_value
        mock_client.embeddings.create.return_value = MagicMock(
            data=[MagicMock(embedding=[0.1] * 1536)]
        )

        source = "knowledge-base.md"
        content = "test text"

        service = VectorService()
        result = service.update_knowledge(source, content)

        mock_client.embeddings.create.assert_called_once_with(
            input="test text",
            model="text-embedding-3-small",
        )
        assert result is True