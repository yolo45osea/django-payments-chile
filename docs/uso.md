# Como Usar

## Instalación

Para utilizar el módulo `django-payments-flow`, puedes realizar la instalación mediante el uso de pip o poetry.

=== "usando pip"
    ```shell
    pip install django-payments-flow
    ```
=== "usando poetry"
    ```shell
    poetry add django-payments-flow
    ```

## Configuración

La configuración del módulo django-payments-flow se realiza como una variante
de Django Payments. Debes agregar la siguiente configuración en tu archivo de
configuración de Django:

```python
PAYMENT_VARIANTS = {
    "flow": ("django_payments_flow.FlowProvider", {
        "api_key": "flow_key",
        "api_secret": "flow_secret",
    })
}
```

Por defecto las llamadas se realizan al ambiente de produccion de Flow, si
quieres realizar llamadas al ambiente sandbox debes agregar
`"endpoint": "sandbox"` a la configuracion

```python
PAYMENT_VARIANTS = {
    "flow": ("django_payments_flow.FlowProvider", {
        "api_key": "flow_key",
        "api_secret": "flow_secret",
        "api_endpoint": "sandbox"
    })
}
```

### Variables de configuración

* `api_endpoint`: Valor de ambiente de Flow, puede ser "live o "sandbox" (Valor por
 defecto: live)
* `api_key`: Este valor corresponde a la cuenta entregada por Flow para
identificar al receptor de los pagos.
* `api_secret`: Este valor corresponde a la contraseña entregada por Khipu para
autenticar la comunicación con su plataforma.
* `api_medio`: Este valor indica si quieres utilizar algun medio de pago especifico
segun lo indicado en
[FlowAPI](https://www.flow.cl/docs/api.html#section/Introduccion/Realizar-pruebas-en-nuestro-ambiente-Sandbox)
(Valor por defecto: 9)

## Datos Extra

El módulo `django-payments-flow` permite enviar datos extra en cada pago. Para
hacerlo, debes utilizar un objeto JSON dentro de la propiedad "attrs" del
modelo de Pagos.

Por ejemplo, si deseas enviar un limite de 5 minutos para cada compra, puedes
utilizar el siguiente código:

```python
datos_extra: dict = {
    "timeout": 300,
}
payment.attrs.datos_extra = datos_extra
payment.save()
```

Puedes proporcionar un diccionario unidimensional con los valores extra que
deseas enviar en cada pago.

Cabe destacar que los valores `apiKey`, `commerceOrder`, `subject`, `amount`,
`email`, `urlConfirmation`, `urlReturn`, `s` no pueden ser utilizados como
datos extra y serán ignorados al momento de crear el pago.
