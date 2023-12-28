from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm
from allauth.account.decorators import verified_email_required
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from emails.models import EmailRecords
from .models import CustomUser
from plans.models import Plan
from .forms import CustomUserPlanChange
from subscriptions.models import Subscription
from emails.forms import SingleEmailForm
from billing.models import Billing


# Create your views here.

@login_required
# @verified_email_required
def user_page(request, user_id=None):
    email_form = SingleEmailForm()
    if user_id:

        if request.user.is_superuser:
            user = CustomUser.objects.get(id=user_id)
        else:
            return HttpResponse("Nice try. You don't belong here!!", status=400)
    else:
        user = request.user

    try:
        subscription = Subscription.objects.filter(user_id=user.id)
        for sub in subscription:
            print(sub.plan_id)
    except ObjectDoesNotExist:
        subscription = []
        pass

    email_list = EmailRecords.objects.filter(user_id=user.id)

    user_details = {'user': user, 'subs': subscription, 'superuser': request.user.is_superuser,'email_form': email_form, 'email_list': email_list}

    return render(request, 'accounts/user_page.html', user_details)


def change_profile(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserPlanChange(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_page')
    else:
        form = CustomUserPlanChange()
    # print(request)
    return render(request, 'accounts/change_profile.html', {'form': form})
