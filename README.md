# django-payments-chile

`django-payments-chile` es una extensión para `django-payments`, una biblioteca que proporciona una interfaz universal para procesar pagos en aplicaciones Django. Este proyecto añade soporte específico para varios proveedores de pagos chilenos como Flow, Khipu, Webpay, y otros.

![PyPI - Status](https://img.shields.io/pypi/status/django-payments-chile)
[![Downloads](https://pepy.tech/badge/django-payments-chile)](https://pepy.tech/project/django-payments-chile)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/fde07768d1714b0b93c6addd5e13bb7f)](https://app.codacy.com/gh/mariofix/django-payments-chile/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/7dc3c8d6fe844fdaa1de0cb86c242934)](https://app.codacy.com/gh/mariofix/django-payments-chile/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/mariofix/django-payments-chile/main.svg)](https://results.pre-commit.ci/latest/github/mariofix/django-payments-chile/main)
![PyPI](https://img.shields.io/pypi/v/django-payments-chile)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-payments-chile)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/django-payments-chile)
![PyPI - License](https://img.shields.io/pypi/l/django-payments-chile)

## Proveedores de pago soportados

- **Flow**: Plataforma chilena para pagos en línea que admite múltiples métodos de pago.
- **Khipu**: Permite pagos mediante transferencia electrónica en tiempo real.
- **Klap**: Solución de pagos electrónicos enfocados en comercios.
- **Kushki**: Proveedor de pagos electrónicos que facilita la integración con diversas plataformas.
- **Payku**: Plataforma de pagos enfocada en pequeñas y medianas empresas.
- **Webpay**: El sistema de pago en línea más utilizado en Chile, operado por Transbank.
- **Onepay**: Pago rápido y seguro usando códigos QR.

## Características

- Soporte para múltiples proveedores de pago en un solo proyecto.
- API consistente para crear, procesar y verificar transacciones.
- Fácil configuración y personalización.
- Documentación clara para desarrolladores.
- Soporte para eventos de éxito, fallo, y reembolsos de pagos.

## Instalación

Para instalar la librería, utiliza pip:

```bash
pip install django-payments-chile[todos]
```

- **flow**: Instala extras para Flow.
- **khipu**: Instala extras para Khipu.
- **todos**: Instala todos los extras.

### Configuración de Proveedores

Agrega las credenciales de los proveedores de pago en tu archivo de configuración:

```python
PAYMENT_VARIANTS = {
    'flow': ('django_payments_chile.FlowProvider', {
        'api_key': 'tu_api_key_flow',
        'secret': 'tu_secret_flow',
    }),
    'webpay': ('django_payments_chile.WebpayProvider', {
        'commerce_code': 'tu_commerce_code_webpay',
        'api_key': 'tu_api_key_webpay',
    }),
}
```

## Uso

AGREGAR INSTALACION Y PASOS DE CONFIGURACION DE DJANGO-PAYMETNTS

## Licencia

Este proyecto está licenciado bajo la licencia [MIT](LICENSE).
