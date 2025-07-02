from django.db import models
from django.contrib.auth.models import User


class Bike(models.Model):
    """Represents a bike available for rental."""

    TYPE_CHOICES = [('road', 'Road'),
        ('mountain', 'Mountain'),
        ('electric', 'Electric'),
        ('trekking', 'Trekking'),
    ]

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    size = models.CharField(max_length=10, null=True, blank=True)
    specification = models.JSONField(default=dict)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        """Returns a string representation of the bike, including its brand and model."""
        return f"{self.brand} - {self.model}"


class Reservation(models.Model):
    """Model representing bike reservation through user."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation by {self.user.username} - {self.bike.name}"

class ChatMessage(models.Model):
    """Model representing a chat message in the system."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_from_consultant = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.user.username} at {self.timestamp}"