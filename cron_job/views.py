from datetime import timedelta,datetime

from django.shortcuts import render
from subscriptions.models import Subscription
# Create your views here.


def billing_alerts(request):
    target_date = datetime.now().date() + timedelta(days=5)
    target_day_of_month = target_date.day
    print(target_day_of_month)
    upcoming_billing = Subscription.objects.filter(activation_date=target_day_of_month)
    print(upcoming_billing)
    return ''