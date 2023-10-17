from django.shortcuts import render
from billing.models import Billing
from datetime import datetime
from dateutil.relativedelta import relativedelta
from accounts.models import CustomUser
from subscriptions.models import Subscription
from django.db.models import Q
from subscriptions.forms import SubscriptionActivateForm
from plans.models import BanAccount


# Create your views here.

def check_monthly_payments(request):
    current_date = datetime.now().date()

    one_month_ago = current_date - relativedelta(months=1)
    overdue_subs = Subscription.objects.exclude(billing__date_of_payment__gte=one_month_ago)

    print("crontab worked")
    print(current_date)
    print(one_month_ago)
    for overdue in overdue_subs:
        print(overdue)

    data = {"overdue_users": overdue_subs, }

    return render(request, "actionables/past-due.html", data)

def activation_queue(request):
    subs_for_activation = Subscription.objects.filter(Q(has_paid=True) & Q(is_cancelled=False) & Q(is_active=False))
    print(subs_for_activation)
    return render(request, "actionables/activate.html", {"subs": subs_for_activation})

def list_of_actives(request):
    active_subs = Subscription.objects.filter(is_active=True)

    return render(request, "actionables/sub_list.html", {"subs": active_subs})

def main_actions(request):
    ban_accounts = BanAccount.objects.all()

    subs_for_activation = Subscription.objects.filter(Q(has_paid=True) & Q(is_cancelled=False) & Q(is_active=False))

    active_subs = Subscription.objects.filter(is_active=True)

    current_date = datetime.now().date()

    one_month_ago = current_date - relativedelta(months=1)

    overdue_subs = Subscription.objects.exclude(billing__date_of_payment__gte=one_month_ago).exclude(is_active=False)

    activate_form = SubscriptionActivateForm()

    data = {"activate": subs_for_activation, "sub_list": active_subs, "past_due": overdue_subs, "ban_accounts": ban_accounts, "activate_form": activate_form}

    return render(request, "actionables/actions_main.html", data)





