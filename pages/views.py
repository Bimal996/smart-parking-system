from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from parking.models import ParkingLot
from reservations.models import Reservation


@login_required
def home(request):
    lots = ParkingLot.objects.filter(is_active=True)[:3]
    reservations = Reservation.objects.filter(user=request.user).select_related("lot", "slot")[:5]
    stats = {
        "total_lots": ParkingLot.objects.filter(is_active=True).count(),
        "total_cities": ParkingLot.objects.filter(is_active=True).values("city").distinct().count(),
    }
    return render(request, "pages/home.html", {"lots": lots, "reservations": reservations, "stats": stats})


def about(request):
    team = [
        {
            "name": "Bimal Mahara",
            "role": "Solo Developer & BITM Student",
            "focus": "Designed and developed the full-stack ParkSmart Nepal system as a student of Sudur Paschimanchal Campus.",
        },
    ]
    milestones = [
        {"title": "Research & Planning", "detail": "Studied Dhangadhi parking pain points and drafted ER diagrams and DFDs for a Nepal-wide system."},
        {"title": "Core Build", "detail": "Implemented multi-app Django architecture with namespaced URLs and MySQL-ready models."},
        {"title": "Payments Integration", "detail": "Wired up eSewa, Khalti, and cash-on-arrival flows with live pricing."},
        {"title": "Polish & Viva Prep", "detail": "Refined the design system, tested edge cases, and prepared the walkthrough."},
    ]
    return render(request, "pages/about.html", {"team": team, "milestones": milestones})


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()
        if name and email and message:
            messages.success(request, "Thanks for reaching out! Our team will get back to you within 24 hours.")
            return redirect("pages:contact")
        messages.error(request, "Please fill in all fields before sending your message.")
    return render(request, "pages/contact.html")
