import uuid
from django.db import models
from pgvector.django import VectorField
from core.models import User

# Create your models here.


class KnowledgeBase(models.Model):
    """Model representing knowledge base for AI assistant using pgvector"""
    content = models.TextField()
    embedding = VectorField(dimensions=1536)
    source = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Knowledge: {self.source}"

class ChatSession(models.Model):
    """Model representing a chat session between a user and a consultant."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_sessions")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Chat session {self.id} - {self.user.username}"

class ChatMessage(models.Model):
    """Model adjusted to LLM (OpenAi/Anthropic) standards."""
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System')
    ]
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, null=True, blank=True, related_name="messages")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    tokens_used = models.IntegerField(null=True, blank=True)
    model_name = models.CharField(max_length=50, default="gpt-4o-mini")

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.role} @ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"