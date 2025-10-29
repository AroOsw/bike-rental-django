from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit
from django.utils.text import slugify
from decimal import Decimal
from cloudinary_storage.storage import MediaCloudinaryStorage


DISCOUNT_14_DAYS = Decimal("0.20")
DISCOUNT_7_DAYS = Decimal("0.15")
DISCOUNT_3_DAYS = Decimal("0.10")

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
    model_description = models.TextField(max_length=2000, blank=True, null=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=255, unique=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand} - {self.model}")
        super().save(*args, **kwargs)


    @property
    def main_instance(self):
        return self.instances.first()


    @property
    def available_sizes(self):
        sizes = self.instances.values_list('size', flat=True).distinct()
        return list(sizes)


    def calculate_rental_price(self, num_days):
        """Calculates rental price based on the number of days. Offers a discount for longer rentals."""
        price_per_day = self.price_per_day

        if num_days >= 14:
            price_per_day *= (1 - DISCOUNT_14_DAYS)
        elif num_days >= 7:
            price_per_day *= (1 - DISCOUNT_7_DAYS)
        elif num_days >= 3:
            price_per_day *= (1 - DISCOUNT_3_DAYS)

        return round(price_per_day, 2)

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
        format="WEBP",
        options={"quality": 85},
        blank=True,
        null=True,
        storage=MediaCloudinaryStorage(),
    )
    img_thumbnail = ImageSpecField(
        source="bike_img",
        processors=[ResizeToFit(300, 200)],
        format="WEBP",
        options={"quality": 75},
    )
    img_slider = ImageSpecField(
        source="bike_img",
        processors=[ResizeToFit(800, 533)],
        format="WEBP",
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
        return f"{self.bike_model.brand} {self.bike_model.model} - Size: {self.size}"

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
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        bike_info = str(self.bike_instance) if self.bike_instance else "Bike unavailable"
        return f"Reservation by {self.user.username} - {bike_info}"

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


class Profile(models.Model):
    """Model representing a User profile."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", default="profile_pics/default_profile.webp")
    birth_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    street_address = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class StravaActivity(models.Model):
    """Model representing activities from strava app."""
    activity_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=200)
    distance = models.FloatField()
    total_elevation = models.FloatField()
    start_date = models.DateTimeField()
    activity_type = models.CharField(max_length=50)
    summary_polyline = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.activity_id} - {self.name} - {self.distance}"