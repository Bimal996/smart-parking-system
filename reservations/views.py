from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from parking.models import ParkingLot

from .forms import ReservationForm
from .models import Reservation


@login_required
def create_reservation(request, slug):
    lot = get_object_or_404(ParkingLot, slug=slug, is_active=True)
    slots = lot.slots.all().order_by("floor", "slot_number")

    if request.method == "POST":
        form = ReservationForm(request.POST, lot=lot)
        if form.is_valid():
            vehicle_type = form.cleaned_data["vehicle_type"]
            start_time = form.cleaned_data["start_time"]
            end_time = form.cleaned_data["end_time"]
            selected_slot_number = form.cleaned_data["selected_slot"]

            hourly_rate = lot.rate_for(vehicle_type)
            duration_hours = max(1, round((end_time - start_time).total_seconds() / 3600))
            total_amount = hourly_rate * duration_hours

            with transaction.atomic():
                available_slot = lot.slots.select_for_update().filter(
                    slot_number=selected_slot_number,
                    status="available",
                ).first()
                if not available_slot:
                    form.add_error("selected_slot", "That parking slot was just taken. Choose another slot.")
                    return render(request, "reservations/create.html", {"lot": lot, "slots": slots, "form": form})

                reservation = form.save(commit=False)
                reservation.user = request.user
                reservation.lot = lot
                reservation.slot = available_slot
                reservation.hourly_rate = hourly_rate
                reservation.total_amount = total_amount
                reservation.save()

                available_slot.status = "reserved"
                available_slot.save(update_fields=["status"])

            messages.success(request, f"Slot {available_slot.slot_number} held for you. Complete payment to confirm.")
            return redirect("payments:choose", reference=reservation.reference)
    else:
        form = ReservationForm(lot=lot, initial={"selected_slot": request.GET.get("slot", "")})

    return render(request, "reservations/create.html", {"lot": lot, "slots": slots, "form": form})


@login_required
def my_bookings(request):
    reservations = Reservation.objects.filter(user=request.user).select_related("lot", "slot")
    return render(request, "reservations/my_bookings.html", {"reservations": reservations})


@login_required
def reservation_detail(request, reference):
    reservation = get_object_or_404(Reservation, reference=reference, user=request.user)
    return render(request, "reservations/detail.html", {"reservation": reservation})


@login_required
def cancel_reservation(request, reference):
    reservation = get_object_or_404(Reservation, reference=reference, user=request.user)
    if request.method == "POST" and reservation.status in ("pending_payment", "confirmed"):
        reservation.status = "cancelled"
        reservation.save(update_fields=["status"])
        if reservation.slot:
            reservation.slot.status = "available"
            reservation.slot.save(update_fields=["status"])
        messages.success(request, f"Reservation {reservation.reference} has been cancelled.")
    return redirect("reservations:my_bookings")
