import uuid

from django.db import models

from reservations.models import Reservation


class Payment(models.Model):
    METHOD_CHOICES = [
        ("esewa", "eSewa"),
        ("khalti", "Khalti"),
        ("cash", "Cash on Arrival"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name="payment")
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    amount = models.PositiveIntegerField()
    transaction_uuid = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    gateway_reference = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_uuid} - {self.reservation.reference} - {self.status}"
