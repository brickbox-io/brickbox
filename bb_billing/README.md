# bb_billing

Contains the billing logic for brickbox.io

## Views

Each event type from stripe is handled by its own view file under the views folder.
| URL                    | View                       | Function              |
|------------------------|----------------------------|-----------------------|
| /stripe/payment_method | views.payment_method_event | Payment method update |
| /stripe/invoice        | views.invoice_event        | Invoice event handler |
