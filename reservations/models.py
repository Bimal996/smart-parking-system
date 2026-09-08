import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse

from parking.models import ParkingLot, ParkingSlot


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("pending_payment", "Pending Payment"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    reference = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations")
    lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name="reservations")
    slot = models.ForeignKey(ParkingSlot, on_delete=models.SET_NULL, null=True, related_name="reservations")
    vehicle_type = models.CharField(max_length=10, choices=ParkingSlot.VEHICLE_CHOICES)
    vehicle_number = models.CharField(max_length=20)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    hourly_rate = models.PositiveIntegerField()
    total_amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending_payment")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = f"SPS-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} - {self.user.username}"

    def get_absolute_url(self):
        return reverse("reservations:detail", kwargs={"reference": self.reference})

    @property
    def duration_hours(self):
        seconds = (self.end_time - self.start_time).total_seconds()
        return max(1, round(seconds / 3600))
