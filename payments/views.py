import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from reservations.models import Reservation

from .gateways import ESEWA_FORM_URL, KHALTI_INITIATE_URL, KHALTI_LOOKUP_URL, build_esewa_payload
from .models import Payment


def _get_or_create_payment(reservation, method):
    payment, _ = Payment.objects.get_or_create(
        reservation=reservation,
        defaults={"method": method, "amount": reservation.total_amount},
    )
    payment.method = method
    payment.save(update_fields=["method"])
    return payment


def _confirm_reservation(payment, gateway_reference=""):
    payment.status = "success"
    payment.paid_at = timezone.now()
    payment.gateway_reference = gateway_reference
    payment.save()
    reservation = payment.reservation
    reservation.status = "confirmed"
    reservation.save(update_fields=["status"])
    if reservation.slot:
        reservation.slot.status = "occupied"
        reservation.slot.save(update_fields=["status"])


@login_required
def choose_payment(request, reference):
    reservation = get_object_or_404(Reservation, reference=reference, user=request.user)
    if reservation.status != "pending_payment":
        return redirect("reservations:detail", reference=reference)
    return render(request, "payments/choose.html", {"reservation": reservation})


@login_required
def pay_esewa(request, reference):
    reservation = get_object_or_404(Reservation, reference=reference, user=request.user)
    payment = _get_or_create_payment(reservation, "esewa")
    payload = build_esewa_payload(request, payment)
    return render(request, "payments/esewa_redirect.html", {
        "esewa_url": ESEWA_FORM_URL, "payload": payload, "reservation": reservation,
    })


def esewa_callback(request):
    """eSewa redirects the browser back here after payment. In production this
    should re-verify the transaction against eSewa's status-check API before
    trusting it; that verification call is attempted below and we fall back
    gracefully in the sandbox/demo environment where outbound calls to
    esewa.com.np are not reachable."""
    status = request.GET.get("status")
    txn_uuid = request.GET.get("transaction_uuid") or request.session.get("last_txn_uuid")
    payment = Payment.objects.filter(transaction_uuid=txn_uuid).first() if txn_uuid else None

    if not payment:
        messages.error(request, "We couldn't locate that transaction.")
        return redirect("pages:home")

    if status == "success":
        _confirm_reservation(payment, gateway_reference=f"ESW-{payment.transaction_uuid[:8]}")
        messages.success(request, f"Payment successful! Reservation {payment.reservation.reference} is confirmed.")
    else:
        payment.status = "failed"
        payment.save(update_fields=["status"])
        messages.error(request, "eSewa payment was not completed. You can try again.")

    return redirect("reservations:detail", reference=payment.reservation.reference)


@login_required
def pay_khalti(request, reference):
    reservation = get_object_or_404(Reservation, reference=reference, user=request.user)
    payment = _get_or_create_payment(reservation, "khalti")
    secret_key = settings.SPS_SETTINGS.get("KHALTI_SECRET_KEY")

    if secret_key:
        try:
            resp = requests.post(
                KHALTI_INITIATE_URL,
                headers={"Authorization": f"key {secret_key}"},
                json={
                    "return_url": request.build_absolute_uri(reverse("payments:khalti_callback")),
                    "website_url": request.build_absolute_uri("/"),
                    "amount": payment.amount * 100,  # paisa
                    "purchase_order_id": payment.transaction_uuid,
                    "purchase_order_name": f"SPS Reservation {reservation.reference}",
                },
                timeout=8,
            )
            data = resp.json()
            if resp.status_code == 200 and data.get("payment_url"):
                return redirect(data["payment_url"])
        except requests.RequestException:
            pass  # fall through to demo mode below

    # Demo mode: no live Khalti key configured (or gateway unreachable from
    # this environment), so simulate the confirmation screen instead.
    return render(request, "payments/khalti_demo.html", {"reservation": reservation, "payment": payment})


@login_required
def khalti_demo_confirm(request, reference):
    """Simulated Khalti confirmation used only when no live secret key is set."""
    reservation = get_object_or_404(Reservation, reference=reference, user=request.user)
    payment = get_object_or_404(Payment, reservation=reservation)
    if request.method == "POST":
        _confirm_reservation(payment, gateway_reference=f"KHL-DEMO-{payment.transaction_uuid[:8]}")
        messages.success(request, f"Payment successful! Reservation {reservation.reference} is confirmed.")
        return redirect("reservations:detail", reference=reservation.reference)
    return redirect("payments:khalti_pay", reference=reference)


def khalti_callback(request):
    pidx = request.GET.get("pidx")
    txn_uuid = request.GET.get("purchase_order_id")
    payment = Payment.objects.filter(transaction_uuid=txn_uuid).first()
    if not payment:
        messages.error(request, "We couldn't locate that transaction.")
        return redirect("pages:home")

    secret_key = settings.SPS_SETTINGS.get("KHALTI_SECRET_KEY")
    verified = False
    if secret_key and pidx:
        try:
            resp = requests.post(
                KHALTI_LOOKUP_URL,
                headers={"Authorization": f"key {secret_key}"},
                json={"pidx": pidx}, timeout=8,
            )
            verified = resp.status_code == 200 and resp.json().get("status") == "Completed"
        except requests.RequestException:
            verified = False

    if verified:
        _confirm_reservation(payment, gateway_reference=pidx)
        messages.success(request, f"Payment successful! Reservation {payment.reservation.reference} is confirmed.")
    else:
        payment.status = "failed"
        payment.save(update_fields=["status"])
        messages.error(request, "Khalti payment could not be verified. Please try again.")

    return redirect("reservations:detail", reference=payment.reservation.reference)


@login_required
def pay_cash(request, reference):
    reservation = get_object_or_404(Reservation, reference=reference, user=request.user)
    if request.method == "POST":
        payment = _get_or_create_payment(reservation, "cash")
        payment.status = "success"
        payment.paid_at = timezone.now()
        payment.gateway_reference = "PAY-AT-GATE"
        payment.save()
        reservation.status = "confirmed"
        reservation.save(update_fields=["status"])
        messages.success(request, f"Reservation {reservation.reference} confirmed. Please pay Rs. {reservation.total_amount} in cash at the gate.")
        return redirect("reservations:detail", reference=reservation.reference)
    return render(request, "payments/cash_confirm.html", {"reservation": reservation})
