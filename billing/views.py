from django.shortcuts import render
from .models import Billing

# Create your views here.
# def payment_webhook(request, key):

def index(request):
    billing_list = Billing.objects.find(user_id=request.user)
    if len(billing_list) > 0:

        return render(request, 'billing/billing_main.html', {'billings': billing_list})
    else:
        return "No billin yet"
