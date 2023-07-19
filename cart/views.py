from django.shortcuts import render, redirect

from .models import Cart
from billing.models import Billing


# Create your views here.

def cart(request, cart_id):
    # Cart.plan_ids.add(plan_id)

    return render(request, 'cart/cart.html')
