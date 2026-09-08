from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import ParkingLot


def lot_list(request):
    lots = ParkingLot.objects.filter(is_active=True)

    city = request.GET.get("city", "")
    query = request.GET.get("q", "")
    feature = request.GET.get("feature", "")

    if city:
        lots = lots.filter(city=city)
    if query:
        lots = lots.filter(Q(name__icontains=query) | Q(address__icontains=query))
    if feature == "ev":
        lots = lots.filter(has_ev_charging=True)
    elif feature == "covered":
        lots = lots.filter(has_covered_parking=True)
    elif feature == "cctv":
        lots = lots.filter(has_cctv=True)

    paginator = Paginator(lots, 6)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "parking/lot_list.html", {
        "page_obj": page_obj,
        "city": city, "query": query, "feature": feature,
        "city_choices": ParkingLot.CITY_CHOICES,
    })


def lot_detail(request, slug):
    lot = get_object_or_404(ParkingLot, slug=slug, is_active=True)
    slots = lot.slots.all().order_by("floor", "slot_number")
    return render(request, "parking/lot_detail.html", {"lot": lot, "slots": slots})
