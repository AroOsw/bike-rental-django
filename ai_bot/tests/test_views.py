import pytest
from django.urls import reverse
from unittest.mock import patch, MagicMock

from openai import embeddings
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_views(test_user, chat_session):
    url = reverse("ask_ai")
    client = APIClient()
    client.force_login(user=test_user)

    with patch("ai_bot.services.OpenAI") as mock_openai_class:
        mock_client = mock_openai_class.return_value

        mock_client.embeddings.create.return_value = MagicMock(
            data=[MagicMock(embedding=[0.1] * 1536)]
        )

        mock_answer = "This is mock answer"
        mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=mock_answer))],
            usage=MagicMock(total_tokens=10)
        )

        response = client.post(url, {
            "session_id": chat_session.id,
            "message": "Hello",
        }, format="json")

    print(f"BŁĄD Z WIDOKU: {response.content}")
    assert response.status_code == 200
    assert response.json()["reply"] == "This is mock answer"

@pytest.mark.django_db
def test_chat_view_empty_message(chat_session, test_user):
    url = reverse("ask_ai")
    client = APIClient()
    client.force_login(user=test_user)

    response = client.post(url, {
        "message": ""
    }, format="json")

    assert response.status_code == 400

@pytest.mark.django_db
def test_views_openai_failure(test_user, chat_session):
    url = reverse("ask_ai")
    client = APIClient()
    client.force_login(user=test_user)

    with patch("ai_bot.services.OpenAI") as mock_openai_class:
        mock_client = mock_openai_class.return_value

        mock_client.embeddings.create.return_value = MagicMock(
            data=[MagicMock(embedding=[0.1] * 1536)]
        )
        mock_client.chat.completions.create.side_effect = Exception("OpenAI is down")

        response = client.post(url, {
            "session_id": chat_session.id,
            "message": "Hello",
        }, format="json")

    assert response.status_code == 503
