# ¿Qué es django-payments-chile?

`django-payments-chile` es una extensión de Django que te permite procesar pagos en Chile fácilmente. Funciona con `django-payments`, que es una biblioteca más general para manejar pagos en Django.

## Paso 1: Preparar tu entorno

Antes de empezar, asegúrate de tener:

1. Python instalado en tu computadora.
2. Django instalado y un proyecto Django creado.

Si no tienes Django, puedes instalarlo con:

```bash
pip install django
```

Y crear un nuevo proyecto Django con:

```bash
django-admin startproject miproyecto
cd miproyecto
```

## Paso 2: Instalar las bibliotecas necesarias

Ahora, vamos a instalar `django-payments` y `django-payments-chile`:

```bash
pip install django-payments django-payments-chile
```

## Paso 3: Configurar tu proyecto Django

### 3.1 Modificar settings.py

Abre el archivo `settings.py` en tu proyecto Django y agrega estas líneas:

```python
INSTALLED_APPS = [
    # ... tus otras apps ...
    "payments",
]

# Configuración para payments
PAYMENT_HOST = 'tudominio.cl'  # Cambia esto por tu dominio real
PAYMENT_USES_SSL = True  # Usa False si no tienes HTTPS
PAYMENT_MODEL = 'pagos.modelos.Pago'

# Configuración para django-payments-chile (ejemplo con Flow)
PAYMENT_VARIANTS = {
    "flow": ("django_payments_chile.FlowProvider", {
        "api_key": "tu_api_key_de_flow",
        "api_secret": "tu_api_secret_de_flow",
    })
}
```

Nota: Reemplaza 'tudominio.cl', 'tu_api_key_de_flow' y 'tu_api_secret_de_flow' con tus datos reales.

### 3.2 Modificar urls.py

Abre el archivo `urls.py` principal de tu proyecto y agrega esta línea:

```python
from django.urls import include, path

urlpatterns = [
    # ... tus otras URLs ...
    path('payments/', include('payments.urls')),
]
```

## Paso 4: Crear un modelo de pago

Crea un nuevo archivo llamado `modelos.py` en una app de tu proyecto (por ejemplo, en una app llamada 'pagos') y agrega este código:

```python
from django.conf import settings
from payments.models import BasePayment

class Pago(BasePayment):
    def get_failure_url(self) -> str:
        return f"https://{settings.PAYMENT_HOST}/payments/{self.pk}/failure"

    def get_success_url(self) -> str:
        return f"https://{settings.PAYMENT_HOST}/payments/{self.pk}/success"
```

No olvides crear la app 'pagos' si no existe:

```bash
python manage.py startapp pagos
```

Y agrégala a INSTALLED_APPS en settings.py:

```python
INSTALLED_APPS = [
    # ... otras apps ...
    "pagos",
]
```

## Paso 5: Usar django-payments-chile en tu vista

Ahora puedes usar django-payments-chile en tus vistas. Aquí tienes un ejemplo:

```python
from django.shortcuts import redirect
from payments import get_payment_model

def crear_pago(request):
    Payment = get_payment_model()
    payment = Payment.objects.create(
        variant='flow',  # Esto debe coincidir con lo que pusiste en PAYMENT_VARIANTS
        description="Pago por Orden #123",
        total=10000,  # Monto en centavos (100 pesos)
        currency='CLP',
        billing_first_name='Juan',
        billing_last_name='Pérez',
        billing_email='juan.perez@example.com',
    )
    return redirect(payment.get_process_url())
```

## Paso 6: Crear las páginas de éxito y fracaso

No olvides crear las páginas a las que se redirigirá después del pago (éxito o fracaso). Puedes hacerlo creando nuevas vistas y templates.

## Consejos finales

1. Siempre prueba en un entorno de desarrollo antes de ir a producción.
2. Mantén seguros tus datos de API (keys, secrets). No los subas a repositorios públicos.
3. Lee la documentación oficial de django-payments y django-payments-chile para más detalles.
4. ¡No dudes en pedir ayuda en foros de Django si te atascas!

Recuerda que cada paso puede requerir más configuración dependiendo de tu proyecto específico.
