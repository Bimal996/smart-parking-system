from django.db import models
from django.urls import reverse


class ParkingLot(models.Model):
    CITY_CHOICES = [
        ("dhangadhi", "Dhangadhi"),
    ]

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    city = models.CharField(max_length=20, choices=CITY_CHOICES)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    image = models.ImageField(upload_to="lots/", blank=True, null=True)
    hourly_rate_bike = models.PositiveIntegerField(default=20, help_text="NPR per hour")
    hourly_rate_car = models.PositiveIntegerField(default=50, help_text="NPR per hour")
    opening_time = models.TimeField(default="06:00")
    closing_time = models.TimeField(default="22:00")
    is_24_hours = models.BooleanField(default=False)
    has_cctv = models.BooleanField(default=True)
    has_covered_parking = models.BooleanField(default=False)
    has_ev_charging = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_city_display()})"

    def get_absolute_url(self):
        return reverse("parking:lot_detail", kwargs={"slug": self.slug})

    @property
    def google_maps_url(self):
        """Open this seeded lot at its stored coordinates in Google Maps."""
        return f"https://www.google.com/maps/search/?api=1&query={self.latitude},{self.longitude}"

    @property
    def total_slots(self):
        return self.slots.count()

    @property
    def available_slots_count(self):
        return self.slots.filter(status="available").count()

    @property
    def occupancy_percent(self):
        total = self.total_slots
        if not total:
            return 0
        return round(((total - self.available_slots_count) / total) * 100)

    def rate_for(self, vehicle_type):
        return self.hourly_rate_bike if vehicle_type == "bike" else self.hourly_rate_car


class ParkingSlot(models.Model):
    VEHICLE_CHOICES = [
        ("bike", "Bike / Scooter"),
        ("car", "Car"),
        ("suv", "SUV / Jeep"),
        ("van", "Van / Microbus"),
        ("truck", "Pickup / Truck"),
    ]
    STATUS_CHOICES = [
        ("available", "Available"),
        ("occupied", "Occupied"),
        ("reserved", "Reserved"),
        ("maintenance", "Under Maintenance"),
    ]

    lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name="slots")
    slot_number = models.CharField(max_length=10, help_text="e.g. A1, B12")
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_CHOICES, default="car")
    floor = models.CharField(max_length=20, default="Ground")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="available")

    class Meta:
        ordering = ["lot", "floor", "slot_number"]
        unique_together = ("lot", "slot_number")

    def __str__(self):
        return f"{self.lot.name} - {self.slot_number}"
