from django.contrib import admin

from .models import ParkingLot, ParkingSlot


class ParkingSlotInline(admin.TabularInline):
    model = ParkingSlot
    extra = 1


@admin.register(ParkingLot)
class ParkingLotAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "total_slots", "available_slots_count", "is_active")
    list_filter = ("city", "is_active", "has_ev_charging", "has_covered_parking")
    search_fields = ("name", "address")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ParkingSlotInline]


@admin.register(ParkingSlot)
class ParkingSlotAdmin(admin.ModelAdmin):
    list_display = ("lot", "slot_number", "vehicle_type", "floor", "status")
    list_filter = ("lot", "vehicle_type", "status")
    search_fields = ("slot_number",)
    list_editable = ("status",)
