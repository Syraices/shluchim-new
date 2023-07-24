from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Cart
from subscriptions.models import Subscription
import os
from billing.models import Billing


# Create your views here.

def cart(request, cart_id):
    # Cart.plan_ids.add(plan_id)
    cart = Cart.objects.get(id=cart_id)
    subs = Subscription.objects.filter(user_id=cart.user_id.id)
    plan_list = []

    for sub in subs:
        if not sub.is_active:
            plan_list += [sub.plan_id]

    form_link = os.getenv('PAY_FORM_LINK')

    data = {'cart': cart, 'plans': plan_list, 'form_link': form_link}

    return render(request, 'cart/cart.html', data)

def webhook_success(request):
    if request.method == 'POST':

        print(request)

        return HttpResponse('valid', status=200)
