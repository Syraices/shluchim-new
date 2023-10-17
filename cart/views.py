from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
from django.shortcuts import render, redirect
from billing.models import Billing
from .models import Cart
from subscriptions.models import Subscription
import os
from billing.models import Billing
from accounts.models import CustomUser


# Create your views here.

def cart(request):
    current_date = datetime.now(timezone.utc)
    one_month_ago = current_date - relativedelta(months=1)
    if request.user.latest_payment >= one_month_ago:
        cart = None
        try:
            cart = Cart.objects.get(user_id=request.user.id)
        except Exception as e:
            print(e)
            pass
        print(cart)
        if cart:
            subs = Subscription.objects.filter(user_id=cart.user_id.id)
            plan_list = []
            total = 0

            for sub in subs:
                if not sub.is_active:
                    plan_list += [sub.plan_id]
                    total += sub.plan_id.price

            form_link = os.getenv('PAY_FORM_LINK')

            data = {'cart': cart, 'plans': plan_list, 'form_link': form_link, 'total': total}
        else:
            data = {'message': "Nothing in your cart"}

        return render(request, 'cart/cart.html', data)
    else:

        return render(request, 'cart/cart.html', {'message': "Please bring your payments up to date to add a new plan"})


def webhook_success(request):
    if request.method == 'POST':
        print(request.body)

        return HttpResponse('valid', status=200)
    else:
        billed = Billing(user_id=request.user, amount=request.GET.get('UMamount'), date_of_payment=datetime.now())
        user = CustomUser.objects.get(id=request.user.id)
        user.latest_payment = datetime.now()
        user.save()
        billed.save()
        cart = Cart.objects.get(user_id=request.user.id)
        subs = Subscription.objects.filter(user_id=request.user.id)
        for sub in subs:
            sub.has_paid = True
            sub.save()
        cart.delete()

        print(request.GET.get('UMamount'))
        return redirect('user_page')

def webhook_fail(request):
    return redirect('cart')

def webhook_response(request):
    print(request)
    return HttpResponse('valid', status=200)
