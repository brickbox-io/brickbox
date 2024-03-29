'''
Returns formated data for the dashboard charts.
'''

from decimal import Decimal

from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from bb_data.models import UserProfile, CryptoSnapshot, FiatSnapshot, CryptoPayout, FiatPayout


@login_required(login_url='/login/')
def crypto_balance_chart(request, colo=0):
    '''
    URL: /data/cryptochart/
    METHOD: AJAX
    Returns json formatted data of the crypto balance since last payout.
    '''
    formated_data = None

    try:
        user_client = UserProfile.objects.get(user = request.user).clients.all()[colo]

        check_last_reset = CryptoSnapshot.objects.filter(
            account_holder = user_client).order_by('-id')
        starting_point = check_last_reset.count()

        total_balance = check_last_reset[0].balance

        # total_balance = 0
        for check in check_last_reset:
            # total_balance = total_balance + check.balance
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

        # print(formated_data)

    except IndexError:
        user_client = None


    return JsonResponse(formated_data, safe=False)


@login_required(login_url='/login/')
def fiat_balance_chart(request, colo=0):
    '''
    URL: /data/fiatchart/
    METHOD: AJAX
    Returns json formatted data of the dollar balance since last payout.
    '''
    formated_data = None

    try:
        user_client = UserProfile.objects.get(user = request.user).clients.all()[colo]

        check_last_reset = FiatSnapshot.objects.filter(account_holder = user_client).order_by('-id')
        starting_point = check_last_reset.count()

        total_balance = check_last_reset[0].balance

        # total_balance = 0
        for check in check_last_reset:
            # total_balance = total_balance + check.balance
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

        # print(formated_data)

    except IndexError:
        user_client = None

    return JsonResponse(formated_data, safe=False)

# @login_required
# def brickbox_breakdown_chart(request, colo=0):
#     '''
#     Work in progress, unot implemented.
#     '''
#     formated_data = None

#     return JsonResponse(formated_data, safe=False)


@login_required(login_url='/login/')
def monthly_breakdown_chart(request, colo=0):
    '''
    URL: /data/monthlybreakdown/
    METHOD: AJAX
    Returns a month to month cumulative amount generated.
    DOES NOT HANDLE YEARS DYNAMICALLY YET
    '''
    formated_data = {}

    years = [2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]

    for year in years:

        try:
            user_client = UserProfile.objects.get(user = request.user).clients.all()[colo]

            crypto_payouts = CryptoPayout.objects.filter(account_holder=user_client)
            fiat_payouts = FiatPayout.objects.filter(account_holder=user_client)

            monthly_payout = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            for payout in crypto_payouts:
                if payout.recorded.year == year:
                    selected_month = payout.recorded.month - 1
                    month_total = monthly_payout[selected_month]
                    try:
                        monthly_payout[selected_month] = month_total + float(payout.dollar_price)
                    except TypeError:
                        monthly_payout[selected_month] = month_total

            for payout in fiat_payouts:
                if payout.recorded.year == year:
                    selected_month = payout.recorded.month - 1
                    month_total = monthly_payout[selected_month]
                    try:
                        monthly_payout[selected_month] = month_total + float(payout.amount)
                    except TypeError:
                        monthly_payout[selected_month] = month_total

            monthly_payout_cleaned = [round(num, 2) for num in monthly_payout]

        except IndexError:
            monthly_payout_cleaned = None

        except UnboundLocalError:
            monthly_payout_cleaned = None

        formated_data[f"{year}"] = monthly_payout_cleaned

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
