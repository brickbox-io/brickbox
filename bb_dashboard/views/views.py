'''views.py for bb_dashboard'''

import datetime

from django import template
from django.template import loader
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from bb_data.models import ( UserProfile,
                            ColocationClient, ResourceTimeTracking, BillingHistory,
                            CustomScript
)
from bb_vm.models import VirtualBrickOwner, GPU, RentedGPU

if settings.DEBUG:
    stripe_pk = settings.STRIPE_PUBLISHABLE_KEY_TEST
else:
    stripe_pk = settings.STRIPE_PUBLISHABLE_KEY

@login_required(login_url='/login/')
def dashboard(request):
    '''
    URL: /dash/
    Method: GET
    Returns the main dash board where a user can see statisics and or create bricks.
    '''
    return render(request, 'dashboard.html')

# -------------------- Backward Compatibility Page Handler ------------------- #
@login_required
def pages(request):
    '''
    Serves the diffrent pages.
    '''
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template

        context['profile'] = UserProfile.objects.get(user = request.user)
        context['bricks'] = VirtualBrickOwner.objects.filter(owner=context['profile'])
        context['scripts'] = CustomScript.objects.filter(user = request.user)
        context['ssh_url'] = settings.SSH_URL

        context['colo_clients'] = ColocationClient.objects.all()

        context['stripe_pk'] = stripe_pk

        context['3090_gpu_available'] = False
        gpu_list = GPU.objects.filter(
                        is_enabled=True, model="3090",
                        host__is_enabled=True, host__is_ready=True
                    )
        for gpu in gpu_list:
            if RentedGPU.objects.filter(gpu=gpu).count() < 1:
                context['3090_gpu_available'] = True

        context['3070_gpu_available'] = False
        gpu_list = GPU.objects.filter(
                        is_enabled=True, model="3070",
                        host__is_enabled=True, host__is_ready=True
                    )
        for gpu in gpu_list:
            if RentedGPU.objects.filter(gpu=gpu).count() < 1:
                context['3070_gpu_available'] = True

        # ------------------------------ Cycyle Balance ------------------------------ #
        tracker, created = ResourceTimeTracking.objects.get_or_create(
                                        user = context['profile'].user,
                                        balance_paid = False,
                                        billing_cycle_end__gte=datetime.datetime.today()
                                    )
        context['billing_history'] = BillingHistory.objects.filter(
                                        user=context['profile'].user).order_by('-id')

        if created:
            tracker.billing_cycle_end = tracker.billing_cycle_start + datetime.timedelta(days=30)
            tracker.save()

        context['tracker'] = tracker

        html_template = loader.get_template( f'{load_template}.html' )
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    # except:

    #     html_template = loader.get_template( 'page-500.html' )
    #     return HttpResponse(html_template.render(context, request))
