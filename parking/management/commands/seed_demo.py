from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from parking.models import ParkingLot, ParkingSlot


LOTS = [
    {
        "name": "Seti Hospital Kailali",
        "city": "dhangadhi",
        "address": "Seti Provincial Hospital, Dhangadhi, Kailali",
        "description": "Convenient parking for patients, visitors, and hospital staff near Seti Provincial Hospital.",
        "latitude": 28.7011, "longitude": 80.5880,
        "hourly_rate_bike": 15, "hourly_rate_car": 40,
        "has_cctv": True, "has_covered_parking": True, "has_ev_charging": True,
        "opening_time": "05:00", "closing_time": "23:00", "is_24_hours": False,
        "slots": [("A", 8, "car"), ("B", 12, "bike")],
    },
    {
        "name": "Bhat Bhateni Supermarket Dhangadhi",
        "city": "dhangadhi",
        "address": "Bhat Bhateni Supermarket, Dhangadhi, Kailali",
        "description": "Customer parking serving shoppers at Bhat Bhateni Supermarket with clear spaces for cars and two-wheelers.",
        "latitude": 28.6947, "longitude": 80.5875,
        "hourly_rate_bike": 10, "hourly_rate_car": 30,
        "has_cctv": True, "has_covered_parking": True, "has_ev_charging": False,
        "opening_time": "07:00", "closing_time": "21:00", "is_24_hours": False,
        "slots": [("A", 12, "car"), ("B", 18, "bike")],
    },
    {
        "name": "Dhangadhi Sub-metropolitan City Kailali",
        "city": "dhangadhi",
        "address": "Dhangadhi Sub-metropolitan City Office, Kailali",
        "description": "Central public parking for visitors accessing the Dhangadhi Sub-metropolitan City office and nearby civic services.",
        "latitude": 28.6958, "longitude": 80.5856,
        "hourly_rate_bike": 10, "hourly_rate_car": 25,
        "has_cctv": True, "has_covered_parking": False, "has_ev_charging": False,
        "opening_time": "06:00", "closing_time": "20:00", "is_24_hours": False,
        "slots": [("A", 10, "car"), ("B", 16, "bike")],
    },
    {
        "name": "Devoti Hotel Dhangadhi",
        "city": "dhangadhi",
        "address": "Devoti Hotel, Dhangadhi, Kailali",
        "description": "Guest and visitor parking beside Devoti Hotel, suitable for short stays and overnight hotel visits.",
        "latitude": 28.6994, "longitude": 80.5859,
        "hourly_rate_bike": 15, "hourly_rate_car": 40,
        "has_cctv": True, "has_covered_parking": True, "has_ev_charging": False,
        "opening_time": "00:00", "closing_time": "23:59", "is_24_hours": True,
        "slots": [("A", 8, "car"), ("B", 10, "bike")],
    },
    {
        "name": "Hotel Rubash Dhangadhi",
        "city": "dhangadhi",
        "address": "Hotel Rubash, Dhangadhi, Kailali",
        "description": "Secure parking for Hotel Rubash guests and visitors close to Dhangadhi's central commercial area.",
        "latitude": 28.6978, "longitude": 80.5842,
        "hourly_rate_bike": 15, "hourly_rate_car": 40,
        "has_cctv": True, "has_covered_parking": True, "has_ev_charging": False,
        "opening_time": "00:00", "closing_time": "23:59", "is_24_hours": True,
        "slots": [("A", 8, "car"), ("B", 10, "bike")],
    },
]


class Command(BaseCommand):
    help = "Replaces parking data with five Dhangadhi, Kailali demo lots and slots."

    def handle(self, *args, **options):
        created_lots = 0
        created_slots = 0

        with transaction.atomic():
            ParkingLot.objects.all().delete()

            for lot_data in LOTS:
                slots_spec = lot_data["slots"]
                lot_fields = {key: value for key, value in lot_data.items() if key != "slots"}
                lot = ParkingLot.objects.create(
                    slug=slugify(lot_fields["name"]),
                    **lot_fields,
                    is_active=True,
                )
                created_lots += 1

                for floor_prefix, count, vehicle_type in slots_spec:
                    for i in range(1, count + 1):
                        number = f"{floor_prefix}{i}"
                        status = "occupied" if (i % 3 == 0) else "available"
                        ParkingSlot.objects.create(
                            lot=lot, slot_number=number, vehicle_type=vehicle_type,
                            floor=floor_prefix, status=status,
                        )
                        created_slots += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seed complete: replaced all parking data with {created_lots} lots and {created_slots} slots."
        ))
