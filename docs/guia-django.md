# Guía para configurar Django con django-payments y django-payments-chile

Esta guía está diseñada para ayudarte a integrar **django-payments** y **django-payments-chile** en una aplicación Django ya funcional que no necesariamente tiene un modulo de pago.

---

## Instalación de dependencias

Dentro de tu proyecto Django, debes usar el administrador de paquetes que mas de guste, esta aplicacion se encuenta publicada en PyPi.

Con `pip`:

```bash
pip install django-payments django-payments-chile
```

Con `poetry`:

```bash
poetry add django-payments django-payments-chile
```

### Crear una aplicación para pagos

Luego utiliza el siguiente comando para crear la aplicación de pagos:

```bash
python manage.py startapp pagos
```

La aplicación `pagos` se utilizará para integrar y extender las funcionalidades de django-payments y django-payments-chile.

---

## Configuración de Django-Payments

### 1. Agregar aplicaciones al archivo `settings.py`

En el archivo de configuración principal de tu proyecto Django, agrega las aplicaciones necesarias:

```python
INSTALLED_APPS = [
    ...
    "payments",
    "pagos",
    ...
]
```

### 2. Configurar los parámetros necesarios

Agrega las configuraciones clave en tu archivo `settings.py`:

```python
PAYMENT_HOST = 'tu-tienda.cl'  # Cambia esto por el dominio de tu aplicación
PAYMENT_USES_SSL = True  # Es recomendable habilitar TLS para mayor seguridad
PAYMENT_MODEL = 'pagos.models.Payment'  # Modelo extendido para pagos

PAYMENT_VARIANTS = {
    "klap": (
        "django_payments_chile.KlapProvider",
        {
            "api_key": "KLAP_KEY",
            "api_secret": "secret",
        }
    )
}
```

### 3. Configurar URLs

Incluye las rutas de django-payments en el archivo de rutas principales de tu proyecto o en un archivo específico como `pagos/urls.py`:

```python
from django.urls import include, path

urlpatterns = [
    ...
    path('payments/', include('payments.urls')),
    ...
]
```

---

## Crear un modelo extendido para Django-Payments

Django-Payments requiere un modelo que extienda la clase base `BasePayment`.

```python
from decimal import Decimal
from django.urls import reverse
from payments import PurchasedItem
from payments.models import BasePayment

class Payment(BasePayment):
    def get_failure_url(self) -> str:
        return reverse('payment_failure', kwargs={'pk': self.pk})

    def get_success_url(self) -> str:
        return reverse('payment_success', kwargs={'pk': self.pk})
```

Este modelo maneja las URLs para redirigir a los usuarios después de un pago exitoso o fallido utilizando rutas nombradas en lugar de construir URLs manualmente.

---

## Crear vistas para manejar éxito y fallos de pago

Es necesario crear vistas que gestionen las respuestas después de un pago exitoso o fallido. Estas vistas se pueden definir dentro de la aplicación `pagos`:

### Ejemplo de vistas

```python
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from pagos.models import Payment

def payment_success(request, pk):
    pago = get_object_or_404(Payment, pk=pk)
    return HttpResponse(f"El pago con ID {pago.pk} fue exitoso. Gracias por tu compra.")

def payment_failure(request, pk):
    pago = get_object_or_404(Payment, pk=pk)
    return HttpResponse(f"El pago con ID {pago.pk} no pudo completarse. Por favor, intenta nuevamente.")
```

### Configurar las rutas para las vistas

Agrega las rutas correspondientes en el archivo `pagos/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('success/<int:pk>/', views.payment_success, name='payment_success'),
    path('failure/<int:pk>/', views.payment_failure, name='payment_failure'),
]
```

Finalmente, incluye estas rutas en las rutas principales del proyecto:

```python
from django.urls import include, path

urlpatterns = [
    ...
    path('pagos/', include('pagos.urls')),
    ...
]
```

---

Con esta configuración, tu aplicación estará lista para manejar los flujos de éxito y fallo en los pagos, integrando **django-payments** y **django-payments-chile** de manera efectiva.
