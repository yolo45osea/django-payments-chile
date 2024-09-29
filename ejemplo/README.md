# Ejemplo para `django-payments-chile`

Este repositorio contiene un ejemplo de cómo utilizar `django-payments-chile`, una extensión de `django-payments` que permite la integración de varios proveedores de pago en Chile.

## Requisitos

- Python 3.10 o superior
- Poetry (para gestionar dependencias)

## Instalación

Sigue los pasos a continuación para poner en marcha el proyecto de ejemplo:

1. Instala las dependencias utilizando `poetry`:

    ```bash
    poetry install -E todo
    ```

2. Aplica las migraciones para preparar la base de datos:

    ```bash
    poetry run python manage.py makemigrations
    poetry run python manage.py migrate
    ```

3. Inicia el servidor de desarrollo:

    ```bash
    poetry run python manage.py runserver
    ```

## Configuración adicional

Este proyecto ya incluye configuraciones predeterminadas para un entorno local. Asegúrate de modificar cualquier valor en el archivo `settings.py` si es necesario, como el dominio en `PAYMENT_HOST`, y las credenciales de los proveedores de pago en `PAYMENT_VARIANTS`.
