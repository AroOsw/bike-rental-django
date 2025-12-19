from django.db import models
from pgvector.django import VectorField
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