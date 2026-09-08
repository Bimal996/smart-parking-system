from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """Extra profile data for each registered user (kept separate from
    django.contrib.auth.User so the built-in auth system stays untouched)."""

    VEHICLE_CHOICES = [
        ("bike", "Bike / Scooter"),
        ("car", "Car"),
        ("suv", "SUV / Jeep"),
        ("van", "Van / Microbus"),
        ("truck", "Pickup / Truck"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True, help_text="e.g. Lakeside, Pokhara")
    default_vehicle_type = models.CharField(
        max_length=10, choices=VEHICLE_CHOICES, default="car"
    )
    default_vehicle_number = models.CharField(
        max_length=20, blank=True, help_text="e.g. GA 2 PA 1234"
    )
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile: {self.user.username}"
