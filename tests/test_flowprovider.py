from unittest import TestCase
from unittest.mock import Mock, patch

import requests
from payments import PaymentError, PaymentStatus, RedirectNeeded

from django_payments_chile.FlowProvider import FlowProvider

API_KEY = "flow_test_key"  # nosec
API_SECRET = "flow_test_secret"  # nosec


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


class TestFlowProviderLive(TestCase):
    def test_provider_create_session_success(self):
        payment = Payment()
        provider = FlowProvider(api_key=API_KEY, api_secret=API_SECRET)
        with patch("django_payments_chile.FlowProvider.requests.post") as mock_post:
            # Configure mock response
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None  # Simulates no exception raised
            mock_response.json.return_value = {"url": "https://flow.cl", "token": "TOKEN_ID", "flowOrder": "ORDER_ID"}
            mock_post.return_value = mock_response

            with self.assertRaises(RedirectNeeded):
                provider.get_form(payment)

            self.assertEqual(payment.status, PaymentStatus.WAITING)
            self.assertEqual(payment.attrs.respuesta_flow["url"], "https://flow.cl")
            self.assertEqual(payment.attrs.respuesta_flow["token"], "TOKEN_ID")
            self.assertEqual(payment.attrs.respuesta_flow["flowOrder"], "ORDER_ID")

    def test_provider_create_session_error(self):
        payment = Payment()
        provider = FlowProvider(api_key=API_KEY, api_secret=API_SECRET)
        with patch("django_payments_chile.FlowProvider.requests.post") as mock_post:
            # Simulate an error response
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("Error occurred")
            mock_post.return_value = mock_response

            with self.assertRaises(PaymentError):
                provider.get_form(payment)

            self.assertEqual(payment.status, PaymentStatus.ERROR)
            self.assertIn("Error occurred", payment.message)

    def test_provider_change_status(self):
        payment = Payment()
        payment.change_status(PaymentStatus.CONFIRMED, "Payment successful")

        self.assertEqual(payment.status, PaymentStatus.CONFIRMED)
        self.assertEqual(payment.message, "Payment successful")

    def test_provider_transaction_id_set(self):
        payment = Payment()
        provider = FlowProvider(api_key=API_KEY, api_secret=API_SECRET)
        with patch("django_payments_chile.FlowProvider.requests.post") as mock_post:
            # Configure mock response with transaction ID
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {"url": "https://flow.cl", "token": "TOKEN_ID", "flowOrder": "ORDER_ID"}
            mock_post.return_value = mock_response

            with self.assertRaises(RedirectNeeded):
                provider.get_form(payment)

            self.assertEqual(payment.transaction_id, "TOKEN_ID")


class TestFlowProviderSandbox(TestCase):
    def test_provider_create_session_success(self):
        payment = Payment()
        provider = FlowProvider(api_key=API_KEY, api_secret=API_SECRET, api_endpoint="sandbox")
        with patch("django_payments_chile.FlowProvider.requests.post") as mock_post:
            # Configure mock response
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None  # Simulates no exception raised
            mock_response.json.return_value = {"url": "https://flow.cl", "token": "TOKEN_ID", "flowOrder": "ORDER_ID"}
            mock_post.return_value = mock_response

            with self.assertRaises(RedirectNeeded):
                provider.get_form(payment)

            self.assertEqual(payment.status, PaymentStatus.WAITING)
            self.assertEqual(payment.attrs.respuesta_flow["url"], "https://flow.cl")
            self.assertEqual(payment.attrs.respuesta_flow["token"], "TOKEN_ID")
            self.assertEqual(payment.attrs.respuesta_flow["flowOrder"], "ORDER_ID")
