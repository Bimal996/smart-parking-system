from django.contrib import admin

from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("reference", "user", "lot", "slot", "vehicle_type", "total_amount", "status", "created_at")
    list_filter = ("status", "vehicle_type", "lot")
    search_fields = ("reference", "user__username", "vehicle_number")
    readonly_fields = ("reference",)
