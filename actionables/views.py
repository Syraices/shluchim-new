from django.shortcuts import render
from billing.models import Billing
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from accounts.models import CustomUser
from subscriptions.models import Subscription
from django.db.models import Q
from subscriptions.forms import SubscriptionActivateForm
from plans.models import BanAccount
from django.utils import timezone
import pytz

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

    cancelled_accounts = Subscription.objects.filter(is_cancelled=True)

    suspended_accounts = Subscription.objects.filter(is_suspended=True)

    subs_for_activation = Subscription.objects.filter(Q(has_paid=True) & Q(is_cancelled=False) & Q(is_active=False))

    active_subs = Subscription.objects.filter(is_active=True)

    current_date = timezone.make_aware(datetime.now())

    overdue_subs = Subscription.objects.prefetch_related('billing_set').filter(is_active=True)
    od_subs_arr = []
    # print(overdue_subs)

    for sub in overdue_subs:
        # print(sub.billing_set.all())
        activation = sub.activation_date
        # print(timezone.is_naive(activation))
        # print(timezone.is_aware(activation))
        # if timezone.is_naive(activation):
        #     activation = timezone.make_aware(activation)
        #     print(activation)
        # print(sub.billing_set.count())

        if sub.billing_set.count() > 0:
            due_date = sub.billing_set.order_by('-date_of_payment').first().date_of_payment
            # activation_date = sub.activation_date
            # print(activation)
            # print(timezone.is_naive(current_date))
            # print(timezone.is_aware(current_date))
            activation_months = relativedelta(current_date, activation).months
            # print(activation_months)
            last_due_date = activation + relativedelta(months=activation_months)
            print(last_due_date)
            if last_due_date > current_date:
                last_due_date = last_due_date - relativedelta(months=1)

            if due_date < last_due_date - relativedelta(months=1):
                suspension_date = due_date + relativedelta(months=1)
                suspension_date = suspension_date.replace(day=activation.day)
                od_subs_arr.append({'sub': sub, 'overdue_date': suspension_date.date()})

            print(last_due_date)
            #
            # print(sub.billing_set.order_by('-date_of_payment').first().date_of_payment)
            # print(due_date)

    activate_form = SubscriptionActivateForm()

    data = {"activate": subs_for_activation, "sub_list": active_subs, "past_due": od_subs_arr,
            "ban_accounts": ban_accounts, "activate_form": activate_form, "suspended_accounts": suspended_accounts,
            "cancelled_accounts": cancelled_accounts}

    return render(request, "actionables/actions_main.html", data)
