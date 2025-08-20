from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit
from django.utils.text import slugify
from decimal import Decimal





class BikeModel(models.Model):
    """Represents a general bike model his specification and available sizes."""

    TYPE_CHOICES = [('road', 'Road'),
        ('mountain', 'Mountain'),
        ('electric', 'Electric'),
        ('trekking', 'Trekking'),
    ]

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    specification = models.JSONField(default=dict, blank=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """Returns a string representation of the bike, including its brand and model."""
        return f"{self.brand} - {self.model}"

    class Meta:
        verbose_name_plural = "Bicycle Models"
        unique_together = ('brand', 'model', 'type')

class BikeInstance(models.Model):
    """Represent specific bike to rent"""

    bike_model = models.ForeignKey(BikeModel, on_delete=models.CASCADE, related_name="instances")
    size = models.CharField(max_length=10)
    serial_number = models.CharField(max_length=100, unique=True)
    bike_img = ProcessedImageField(
        upload_to="upload/bikes",
        processors=[ResizeToFit(1600, 1066)],
        format="JPEG",
        options={"quality": 85},
        blank=True,
        null=True,
    )
    img_thumbnail = ImageSpecField(
        source="bike_img",
        processors=[ResizeToFit(300, 200)],
        format="JPEG",
        options={"quality": 75},
    )
    img_slider = ImageSpecField(
        source="bike_img",
        processors=[ResizeToFit(800, 533)],
        format="JPEG",
        options={"quality": 80},
    )

    STATUS_CHOICES = [
        ("available", "Available"),
        ("rented", "Rented"),
        ("maintenance", "Maintenance"),
        ("retired", "Retired"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")

    def __str__(self):
        return f"{self.bike_model.brand} {self.bike_model.model} - Size: {self.size} - S/N {self.serial_number}"

    class Meta:
        verbose_name_plural = "Bicycle Instances"
        ordering = ['bike_model__brand', 'bike_model__model', 'size']


class Reservation(models.Model):
    """Model representing bike reservation through user."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike_instance = models.ForeignKey(BikeInstance, on_delete=models.CASCADE, related_name="reservations")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        bike_info = str(self.bike_instance) if self.bike_instance else "Bike unavailable"
        return f"Reservation by {self.user.username} - {bike_info} from {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    def calculate_total_cost(self):
        """Calculates the total cost of the reservation."""
        if self.start_time and self.end_time and self.bike_instance:
            num_days = (self.end_time.date() - self.start_time.date()).days + 1

            if num_days < 1:
                num_days = 1

            self.total_cost = self.bike_instance.bike_model.price_per_day * Decimal(num_days)
        else:
            self.total_cost = Decimal("0.00")

    def save(self, *args, **kwargs):
        """Overrides the save method to automatically calculate total cost."""
        self.calculate_total_cost()
        super().save(*args, **kwargs)


class ChatMessage(models.Model):
    """Model representing a chat message in the system."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_from_consultant = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.user.username} at {self.timestamp}"


def page_image_path(instance, filename):
    """Dynamic path for storing images based on page_section and slug."""
    return f"{instance.page_section}/{instance.slug}/{filename}"


class PageImages(models.Model):
    """Model representing images for pages."""
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    page_section = models.CharField(max_length=100, blank=True, help_text="e.g., homepage, about, bikes")
    original_image = models.ImageField(upload_to=page_image_path, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
    ])

    # Predefined image specs for common use cases
    hero_webp = ImageSpecField(
        source='original_image',
        processors=[ResizeToFit(1920, 1080)],
        format='WEBP',
        options={'quality': 80},
    )
    thumbnail_webp = ImageSpecField(
        source='original_image',
        processors=[ResizeToFit(300, 300)],
        format='WEBP',
        options={'quality': 70},
    )

    def __str__(self):
        return f"{self.title} ({self.page_section})"

    def save(self, *args, **kwargs):
        """Automatically generate slug from title if not provided."""
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=False).replace('-', '-')
            original_slug = self.slug
            count = 1
            while PageImages.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}_{count}"
                count += 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Page Image'
        verbose_name_plural = 'Page Images'