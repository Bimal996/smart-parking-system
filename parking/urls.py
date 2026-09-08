from django.urls import path

from . import views

app_name = "parking"

urlpatterns = [
    path("", views.lot_list, name="lot_list"),
    path("<slug:slug>/", views.lot_detail, name="lot_detail"),
]
