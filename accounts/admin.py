from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "default_vehicle_type", "default_vehicle_number")
    search_fields = ("user__username", "user__email", "phone_number", "default_vehicle_number")
    list_filter = ("default_vehicle_type",)
