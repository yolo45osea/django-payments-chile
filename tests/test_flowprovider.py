from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

from payments import PaymentStatus
from payments import RedirectNeeded

from django_payments_chile import FlowProvider

API_KEY = "flow_test_key"
API_SECRET = "flow_test_secret"


class payment_attrs:
    session = dict


class Payment(Mock):
    id = 1
    description = "payment"
    currency = "CLP"
    delivery = 0
    status = PaymentStatus.WAITING
    message = None
    tax = 0
    total = 5000
    captured_amount = 0
    transaction_id = None
    billing_email = "correo@usuario.com"
    attrs = payment_attrs()

    def change_status(self, status, message=""):
        self.status = status
        self.message = message

    def get_failure_url(self):
        return "http://mi-app.cl/error"

    def get_process_url(self):
        return "http://mi-app.cl/process"

    def get_purchased_items(self):
        return []

    def get_success_url(self):
        return "http://mi-app.cl/exito"


class TestStripeProviderV3(TestCase):
    def test_provider_create_session_success(self):
        payment = Payment()
        provider = FlowProvider(api_key=API_KEY, api_secret=API_SECRET)
        return_value = {"url": "https://flow.cl", "token": "TOKEN_ID", "flowOrder": "ORDER_ID"}
        with patch("stripe.checkout.Session.create", return_value=return_value):
            with self.assertRaises(RedirectNeeded):
                provider.get_form(payment)
                self.assertTrue("url" in payment.attrs.session)
                self.assertTrue("token" in payment.attrs.session)
        self.assertEqual(payment.status, PaymentStatus.WAITING)
