# bb_billing

Contains the billing logic to enforce the brickbox.io billing policy. Payment related interfaces are maintained under the corrisponding dashboard locations.

## Endpoints

Each event type from stripe is handled by its own view file under the views folder.
| URL                    | View                       | Function              |
|------------------------|----------------------------|-----------------------|
| /stripe/account        | views.account_event        | Account event handler |
| /stripe/payment_method | views.payment_method_event | Payment method update |
| /stripe/invoice        | views.invoice_event        | Invoice event handler |

## Billing Policy

### Account Strikes

To determine if an account is place on the payment tier or the credit method a three strike system is used.

### Payment Tiers

New user accounts or accounts with strikes are billed at the following tiers:

**$1** - Any unsucessful payments result in an imediate account suspension. The VM is shutdown and the user has 24 hours to provide a valid payment method. The user receives *three (3) strikes* resulting in their account being imeditly transfered to the credit method with a $100 minimum to maintain their account.

**$10** - Any unsucessful payments will result in the VM being suspended, the user has 48 hours to provide a valid payment method. *Two (2) strikes* to their account is issued and if it occurs again the account to transfered to the credit method.

**$100** - Upon an unsucessful payment the VM is suspended, the user has 5 business days to provide a valid payment method. *One (1) strike* is issued to their account and if it occurs again the account is transfered to the credit method.

**$1,000** - Upon an unsucessful payment the user is given 24 hours to provied a valid payment method before the VM is suspended. Once the VM is suspended the user has 3 business days to pay the balance of their account. Each day that passes the user recieves a strike. If the user fails to pay the balance of their account the account is transfered to the credit method.

**Monthly** - After a sucessful $1,000 payment method accounts are transfered to the monthly payment tier. Upon an unsucessful payment the user has 48 hours to provide a valid payment method before their VM is suspended. They then have 3 business days to pay the balance of their account. If the user fails to pay the balance of their account the account is transfered to the credit method. Sucessful payments at this tier will clear any strikes on the account.

### Credit Method

Users that have a history of unsucessful payments are given a credit method to use to pay for their account.
