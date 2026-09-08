from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("<str:reference>/", views.choose_payment, name="choose"),
    path("<str:reference>/esewa/", views.pay_esewa, name="esewa_pay"),
    path("esewa/callback/", views.esewa_callback, name="esewa_callback"),
    path("<str:reference>/khalti/", views.pay_khalti, name="khalti_pay"),
    path("<str:reference>/khalti/demo-confirm/", views.khalti_demo_confirm, name="khalti_demo_confirm"),
    path("khalti/callback/", views.khalti_callback, name="khalti_callback"),
    path("<str:reference>/cash/", views.pay_cash, name="cash_pay"),
]
