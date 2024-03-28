from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from actionables.forms import CreatePortForm
from .forms import CustomUserChangeForm, CustomUserChangeAdminForm
from allauth.account.decorators import verified_email_required
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from emails.models import EmailRecords, Email
from .models import CustomUser
from plans.models import Plan
from .forms import CustomUserPlanChange
from subscriptions.models import Subscription
from emails.forms import SingleEmailForm, EmailForm
from billing.models import Billing, paymentProfile
from billing.forms import PaymentProfileForm
from utils import get_payment_profiles


# Create your views here.

@login_required
# @verified_email_required
def user_page(request, user_id=None):
    email_form = SingleEmailForm()
    canned_form = EmailForm()
    canned_emails = Email.objects.filter(canned=True)
    profile_form = CustomUserChangeForm()

    if user_id:
        if request.user.is_superuser:
            user = CustomUser.objects.get(id=user_id)

            init_data = {
               'username': user.username,
               'ship_fname': user.ship_fname,
               'ship_lname': user.ship_lname,
               'email': user.email,
               'is_active': user.is_active,
               'phone_number': user.phone_number,
               'four_pin': user.four_pin,
               'ship_address': user.ship_address,
               'ship_city': user.ship_city,
               'ship_state': user.ship_state,
               'ship_zip': user.ship_zip,
               'is_billing': user.is_billing,
            }
            profile_form = CustomUserChangeAdminForm(initial=init_data, instance=user)
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
    port_form = CreatePortForm()

    email_list = EmailRecords.objects.filter(user_id=user.id)

    pay_profiles = paymentProfile.objects.filter(user_id=user.id)
    pay_ops_list = []

    for profile in pay_profiles:
        pay_ops_list.append(get_payment_profiles(user.authnet_id, profile.profile_number))

    print(pay_ops_list)
    pay_profile_form = PaymentProfileForm()

    user_details = {
        'user_id': user,
        'sub_list': subscription,
        'superuser': request.user.is_superuser,
        'email_form': email_form,
        'canned_form': canned_form,
        'email_list': email_list,
        'canned_emails': canned_emails,
        'port_form': port_form,
        'profile_form': profile_form,
        'pay_list': pay_ops_list,
        'pay_profile_form': pay_profile_form
    }

    return render(request, 'accounts/user_page.html', user_details)


def change_profile(request, user_id=None):
    form = CustomUserChangeForm()
    if request.method == 'POST':
        if request.user.is_superuser:
            user = CustomUser.objects.get(id=user_id)
            form = CustomUserChangeAdminForm(request.POST, instance=user)
        else:
            user = request.user
            form = CustomUserChangeForm(request.POST, instance=user)

        if form.is_valid():
            saved_form = form.save()
            if user_id:
                return redirect('admin_user_page', user_id=user_id)
            else:
                return redirect('user_page')
        else:
            return HttpResponse(f"didnt work{form.errors}")
    else:
        return render(request, 'accounts/change_profile.html', {'form': form})
