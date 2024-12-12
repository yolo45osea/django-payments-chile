from dataclasses import asdict, dataclass
from typing import Any, Optional

import requests
from django.http import HttpResponseBadRequest, JsonResponse
from payments import PaymentError, PaymentStatus, RedirectNeeded
from payments.core import BasicProvider, get_base_url


@dataclass
class NuevaTransaccion:
    email: str
    order: str
    subject: str
    amount: int
    currency: str
    payment: int
    expired: str
    urlreturn: str
    urlnotify: str
    additional_parameters: Optional[dict[str, str]] = None


@dataclass
class RespuestaTransaccion:
    status: str
    id: str
    url: str


class PaykuProvider(BasicProvider):
    """
    Proveedor de pagos para Payku.

    Esta clase extiende BasicProvider para proporcionar funcionalidad
    específica para la integración con la API de Payku.
    """

    token_publico: str
    token_privado: str
    site: str
    payment: int = 99

    def __init__(self, token_publico: str, token_privado: str, site: str, **kwargs):
        """
        Inicializa el proveedor de Payku.

        Args:
            token_publico (str): Token público proporcionado por Payku.
            token_privado (str): Token privado proporcionado por Payku.
            site (str): Endpoint de la API de Payku. Puede ser "production" o "sandbox".
            **kwargs: Argumentos adicionales.
        """
        super().__init__(**kwargs)
        self.token_publico = token_publico
        self.token_privado = token_privado
        self.site = site

        if self.site == "production":
            self.site = "https://app.payku.cl/api"
        elif self.site == "sandbox":
            self.site = "https://des.payku.cl/api"

    def get_form(self, payment, data: Optional[dict] = None) -> Any:
        """
        Genera el formulario de pago para redirigir a la página de pago de Payku.

        Args:
            payment ("Payment"): Objeto de pago Django Payments.
            data (dict | None): Datos del formulario (opcional).

        Returns:
            Any: Formulario de pago redirigido a la página de pago de Payku.

        Raises:
            RedirectNeeded: Redirige a la página de pago de Payku.

        """
        if not payment.transaction_id:
            datos_para_payku = NuevaTransaccion(
                email=payment.billing_email,
                order=payment.token,
                urlreturn=payment.get_success_url(),
                urlnotify=f"{get_base_url()}{payment.get_process_url()}",
                subject=payment.description,
                amount=int(payment.total),
                payment=int(self.payment),
                currency=payment.currency,
                additional_parameters=self._extra_data(payment.attrs),
            )

            try:
                payment.attrs.datos_nueva_transaccion = datos_para_payku
                payment.save()
            except Exception as e:
                raise PaymentError(f"Ocurrió un error al guardar attrs.datos_nueva_transaccion: {e}")

            try:
                url = f"{self.site}/api/transaction"
                payku_response = requests.post(url, data=asdict(datos_para_payku))
                payku_response.raise_for_status()

            except Exception as pe:
                payment.change_status(PaymentStatus.ERROR, str(pe))
                raise PaymentError(pe)
            else:
                payment.transaction_id = payku_response.token
                payment.attrs.respuesta_payku = payku_response.json()
                payment.save()
                payment.change_status(PaymentStatus.WAITING)

            raise RedirectNeeded(f"{payku_response.url}?token={payku_response.token}")

    def process_data(self, payment, request) -> JsonResponse:
        """
        Procesa los datos del pago recibidos desde Payku.

        Args:
            payment ("Payment"): Objeto de pago Django Payments.
            request ("HttpRequest"): Objeto de solicitud HTTP de Django.

        Returns:
            JsonResponse: Respuesta JSON que indica el procesamiento de los datos del pago.

        """
        if "id" not in request.POST:
            raise HttpResponseBadRequest("id no está en post")

        data = {"status": "ok"}
        if payment.status in [PaymentStatus.WAITING, PaymentStatus.PREAUTH]:
            self.actualiza_estado(payment=payment)

        return JsonResponse(data)

    def actualiza_estado(self, payment) -> dict:
        """Actualiza el estado del pago con Payku

        Args:
            payment ("Payment): Objeto de pago Django Payments.

        Returns:
            dict: Diccionario con valores del objeto `PaymentStatus`.
        """

        try:
            url = f"{self.site}/api/transaction/{payment.token}"
            status = requests.get(url)
            status.raise_for_status()
        except Exception as e:
            raise e
        else:
            if status.status == "success":
                payment.change_status(PaymentStatus.CONFIRMED)
            elif status.status == "rejected":
                payment.change_status(PaymentStatus.REJECTED)
        return asdict(status)

    def _extra_data(self, attrs) -> dict:
        """Busca los datos que son enviandos por django-payments y los saca del diccionario

        Args:
            attrs ("PaymentAttributeProxy"): Obtenido desde PaymentModel.extra_data

        Returns:
            dict: Diccionario con valores permitidos.
        """
        try:
            data = attrs.datos_extra
        except AttributeError:
            return {}

        prohibidos = [
            "order",
            "urlreturn",
            "urlnotify",
            "subject",
            "amount",
            "payment",
            "currency",
        ]
        for valor in prohibidos:
            if valor in data:
                del data[valor]

        return data

    def refund(self, payment, amount: Optional[int] = None) -> int:
        """
        Realiza un reembolso del pago.
        El seguimiendo se debe hacer directamente en Payku

        Args:
            payment ("Payment"): Objeto de pago Django Payments.
            amount (int | None): Monto a reembolsar (opcional).

        Returns:
            int: Monto de reembolso solicitado.

        Raises:
            PaymentError: Error al crear el reembolso.

        """
        if payment.status != PaymentStatus.CONFIRMED:
            raise PaymentError("El pago debe estar confirmado para reversarse.")

        to_refund = amount or payment.total
        try:
            datos_reembolso = {
                "apiKey": self.api_key,
                "refundCommerceOrder": payment.token,
                "receiverEmail": payment.billing_email,
                "amount": to_refund,
                "urlCallBack": f"{get_base_url()}{payment.get_process_url()}",
                "commerceTrxId": payment.token,
                "flowTrxId": payment.attrs.respuesta_flow["flowOrder"],
            }
            refund = datos_reembolso
        except Exception as pe:
            raise PaymentError(pe)
        else:
            payment.attrs.solicitud_reembolso = refund
            payment.save()
            payment.change_status(PaymentStatus.REFUNDED)
            return to_refund

    def capture(self):
        """
        Captura el pago (no implementado).

        Note:
            Método no soportado por Payku.

        Raises:
            NotImplementedError: Método no implementado.
        """
        raise NotImplementedError()

    def release(self):
        """
        Libera el pago (no implementado).

        Note:
            Método no soportado por Payku.

        Raises:
            NotImplementedError: Método no implementado.

        """
        raise NotImplementedError()
