from django.urls import path

from . import views

app_name = "reservations"

urlpatterns = [
    path("book/<slug:slug>/", views.create_reservation, name="create"),
    path("mine/", views.my_bookings, name="my_bookings"),
    path("<str:reference>/", views.reservation_detail, name="detail"),
    path("<str:reference>/cancel/", views.cancel_reservation, name="cancel"),
]
