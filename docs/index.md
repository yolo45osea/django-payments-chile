# django-payments-chile

**django-payments-chile** es una extensión de **django-payments** que facilita la integración de proveedores de pago en aplicaciones Django para el mercado chileno. Actualmente soporta Flow, Khipu, Webpay, y más.

## Características

- Soporte para múltiples proveedores de pago en Chile.
- Compatible con la API de django-payments.
- Extensión fácil de configurar.

## Inicio rápido

### Instalación

Asegúrate de tener `django-payments` instalado, luego instala `django-payments-chile`:

```bash
pip install django-payments django-payments-chile
```

### Configuración

En tu archivo `settings.py`, configura los proveedores de pago que vas a utilizar:

```python
PAYMENT_VARIANTS = {
    'flow': ('payments_chile.flow.FlowProvider', {
        'api_key': 'tu_api_key_flow',
        'secret': 'tu_secret_flow',
    }),
    'webpay': ('payments_chile.webpay.WebpayProvider', {
        'commerce_code': 'tu_commerce_code_webpay',
        'api_key': 'tu_api_key_webpay',
    }),
    # Otros proveedores como khipu, klap, etc.
}
```

Asegúrate de haber agregado `payments` a `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...,
    'payments',
    'payments_chile',
]
```

### Creación de un nuevo pago

Con django-payments ya configurado, puedes crear un nuevo pago utilizando los métodos nativos de la librería:

```python
from payments import get_payment_model

Payment = get_payment_model()

payment = Payment.objects.create(
    variant='flow',  # o 'webpay', 'khipu', etc.
    description="Pago por Orden #123",
    total=10000,
    currency='CLP',
    billing_first_name='Juan',
    billing_last_name='Pérez',
    billing_email='juan.perez@example.com',
)

# Redirige al usuario al proveedor de pagos
redirect_url = payment.get_process_url()
return redirect(redirect_url)
```

**Nota**: `django-payments` manejará la redirección al proveedor y la confirmación del estado del pago. Solo necesitas configurar correctamente los proveedores.

Para más detalles sobre el flujo de pago y las respuestas de los proveedores, consulta la sección [configuración](configuration.md).

## Proveedores soportados

- Flow
- Khipu
- Klap
- Kushki
- Payku
- Webpay
- Onepay

Consulta la documentación para aprender cómo integrarlos.
