'''
Returns formated data for the dashboard charts.
'''

from decimal import Decimal

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from bb_data.models import UserProfile, CryptoSnapshot, FiatSnapshot


@csrf_exempt
def crypto_balance_chart(request):
    '''
    URL: /data/cryptochart/
    METHOD: AJAX
    Returns json formatted data of the crypto balance since last payout.
    '''

    try:
        user_client = UserProfile.objects.get(user = request.user).clients.all()[0]

        check_last_reset = CryptoSnapshot.objects.filter(
            account_holder = user_client).order_by('-id')
        starting_point = check_last_reset.count()
        total_balance = 0
        for check in check_last_reset:
            total_balance = total_balance + check.balance
            if check.start_period:
                break
            starting_point = starting_point - 1

        if starting_point > 0:
            starting_point = starting_point - 1

        crypto_balance = CryptoSnapshot.objects.filter(
            account_holder = user_client).values()[starting_point:]

        formated_balances = []
        formated_dates = []
        for balance in crypto_balance:
            formated_balances.append(Decimal(balance['balance']).normalize())
            formated_dates.append(f'{balance["recorded"].month}/{balance["recorded"].day}')

        formated_data = {
            'date': formated_dates,
            'ammount': formated_balances,
            'total': Decimal(total_balance).normalize()
        }


        print(formated_data)

    except IndexError:
        user_client = None


    return JsonResponse(formated_data, safe=False)


@csrf_exempt
def fiat_balance_chart(request):
    '''
    URL: /data/fiatchart/
    METHOD: AJAX
    Returns json formatted data of the dollar balance since last payout.
    '''

    try:
        user_client = UserProfile.objects.get(user = request.user).clients.all()[0]

        check_last_reset = FiatSnapshot.objects.filter(account_holder = user_client).order_by('-id')
        starting_point = check_last_reset.count()
        total_balance = 0
        for check in check_last_reset:
            total_balance = total_balance + check.balance
            if check.start_period:
                break
            starting_point = starting_point - 1

        if starting_point > 0:
            starting_point = starting_point - 1

        crypto_balance = FiatSnapshot.objects.filter(
            account_holder = user_client).values()[starting_point:]

        formated_balances = []
        formated_dates = []
        for balance in crypto_balance:
            formated_balances.append(Decimal(balance['balance']).normalize())
            formated_dates.append(f'{balance["recorded"].month}/{balance["recorded"].day}')

        formated_data = {
            'date': formated_dates,
            'ammount': formated_balances,
            'total': Decimal(total_balance).normalize()
        }


        print(formated_data)

    except IndexError:
        user_client = None


    return JsonResponse(formated_data, safe=False)

# @csrf_exempt
# def cumulative_earned(request):
#     try:
#         user_client = UserProfile.objects.get(user = request.user).clients.all()[0]

#         crypto_transactions = CryptoSnapshot.objects.filter(account_holder = user_client)

#         cryto_running_total = 0
#         for transaction in crypto_transactions:
#             cryto_running_total = cryto_running_total + transaction.dollar_price

#         fiat_transactions = FiatSnapshot.objects.filter(account_holder = user_client)

#         fiat_running_total = 0
#         for transaction in fiat_transactions:
#             fiat_running_total = fiat_running_total + transaction.balance

#     except IndexError:
#         user_client = None
