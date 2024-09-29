from django.shortcuts import redirect
from payments import get_payment_model


def crear_pago(request):
    Payment = get_payment_model()
    payment = Payment.objects.create(
        variant="flow",  # Debe coincidir con el nombre en PAYMENT_VARIANTS
        description="Pago por Orden #123",
        total=10000,  # Monto en centavos (100 pesos)
        currency="CLP",
        billing_first_name="Juan",
        billing_last_name="Pérez",
        billing_email="juan.perez@example.com",
    )
    # Redirige al usuario a la URL del proveedor de pagos
    return redirect(payment.get_process_url())
