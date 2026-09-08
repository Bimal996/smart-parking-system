"""
Payment gateway helpers for eSewa (ePay v2) and Khalti (KPG-2).

These build the real request payloads/signatures used by the official
Nepali gateways. When no live merchant credentials are configured in
settings (SPS_SETTINGS), the views fall back to a clearly-labelled demo
flow so the project stays runnable for a viva/demo without live keys.
"""
import base64
import hashlib
import hmac

from django.conf import settings
from django.urls import reverse


def esewa_signature(total_amount, transaction_uuid, product_code):
    """eSewa ePay v2 requires an HMAC-SHA256 signature (base64) over a
    fixed, comma-separated field string, signed with the merchant secret."""
    secret_key = "8gBm/:&EnhH.1/q" if settings.SPS_SETTINGS["ESEWA_MERCHANT_CODE"] == "EPAYTEST" else settings.SPS_SETTINGS.get("ESEWA_SECRET_KEY", "")
    message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    digest = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
    return base64.b64encode(digest).decode()


def build_esewa_payload(request, payment):
    """Return the form fields eSewa's ePay v2 endpoint expects."""
    product_code = settings.SPS_SETTINGS["ESEWA_MERCHANT_CODE"]
    success_url = request.build_absolute_uri(reverse("payments:esewa_callback")) + "?status=success"
    failure_url = request.build_absolute_uri(reverse("payments:esewa_callback")) + "?status=failure"

    return {
        "amount": payment.amount,
        "tax_amount": 0,
        "total_amount": payment.amount,
        "transaction_uuid": payment.transaction_uuid,
        "product_code": product_code,
        "product_service_charge": 0,
        "product_delivery_charge": 0,
        "success_url": success_url,
        "failure_url": failure_url,
        "signed_field_names": "total_amount,transaction_uuid,product_code",
        "signature": esewa_signature(payment.amount, payment.transaction_uuid, product_code),
    }


ESEWA_FORM_URL = "https://rc-epay.esewa.com.np/api/epay/main/v2/form"  # UAT/test endpoint
KHALTI_INITIATE_URL = "https://a.khalti.com/api/v2/epayment/initiate/"
KHALTI_LOOKUP_URL = "https://a.khalti.com/api/v2/epayment/lookup/"
