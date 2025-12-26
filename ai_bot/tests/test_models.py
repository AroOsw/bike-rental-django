import pytest
from ai_bot.models import ChatMessage, KnowledgeBase
from ai_bot.tests.conftest import chat_session


@pytest.mark.django_db
def test_create_message(chat_session):
    content = "Hello assistant"

    message = ChatMessage.objects.create(
        role="user",
        session=chat_session,
        content=content,
    )

    assert message.content == content
    assert message.session.user.username == "test_user"

@pytest.mark.django_db
def test_number_and_order_of_messages(chat_session):

    first_message = "My name is testuser"
    second_message = "Hello testuser"
    third_message = "What is my name"

    message_1 = ChatMessage.objects.create(
        role="user",
        session=chat_session,
        content=first_message,
    )

    message_2 = ChatMessage.objects.create(
        role="assistant",
        session=chat_session,
        content=second_message,
    )

    message_3 = ChatMessage.objects.create(
        role="user",
        session=chat_session,
        content=third_message,
    )

    assert chat_session.messages.count() == 3
    assert chat_session.messages.first().content == "My name is testuser"

@pytest.mark.django_db
def test_vector_size(knowledge_base):

    get_kb = KnowledgeBase.objects.get(id=knowledge_base.id)

    assert len(get_kb.embedding) == 1536

@pytest.mark.django_db
def test_models_string_representation(chat_session, knowledge_base):

    message = ChatMessage.objects.create(
        role="user", session=chat_session, content="test",
    )
    assert str(message) == f"{message.role} @ {message.timestamp.strftime('%Y-%m-%d %H:%M')}"
    assert str(chat_session) == f"Chat session {chat_session.id} - {chat_session.user.username}"
    assert str(knowledge_base) == f"Knowledge: {knowledge_base.source}"

@pytest.mark.django_db
def test_session_cascade_delete(chat_session):
    message = ChatMessage.objects.create(
        role="user", session=chat_session, content="test")

    assert chat_session.messages.count() == 1
    chat_session.delete()
    assert ChatMessage.objects.count() == 0

