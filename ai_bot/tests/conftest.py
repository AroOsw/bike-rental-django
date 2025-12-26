import pytest
from django.contrib.auth import get_user_model
from ai_bot.models import ChatSession, KnowledgeBase

User = get_user_model()

@pytest.fixture
def test_user(db):
    """Create and return test user"""
    return User.objects.create_user(username="test_user", password="password123")

@pytest.fixture
def chat_session(db, test_user):
    """Create chat session assigned to test_user"""
    return ChatSession.objects.create(user=test_user)

@pytest.fixture
def knowledge_base(db):
    return KnowledgeBase.objects.create(
        content="test text",
        embedding=[0.1] * 1536,
        source="knowledge_base.md",
    )
