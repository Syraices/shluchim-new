from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
from django.shortcuts import render, redirect

from coupon.models import Coupon
from .forms import CartCouponForm
from .models import Cart
from subscriptions.models import Subscription
import os
from billing.models import Billing
from billing.forms import PaymentProfileForm
from accounts.models import CustomUser
import json
import urllib.parse
from utils import charge_cc, create_customer_profile, charge_existing_customer, get_payment_profiles


# Create your views here.

def cart(request):
    form = CartCouponForm()
    current_date = datetime.now(timezone.utc)
    one_month_ago = current_date - relativedelta(months=1)
    # if hasattr(request.user, 'latest_payment') and request.user.latest_payment and request.user.latest_payment >= one_month_ago:
    cart = None
    try:
        cart = Cart.objects.get(user_id=request.user.id)
    except Exception as e:
        print(e)
        pass
    print(cart)
    if cart:
        subs = Subscription.objects.filter(user_id=request.user.id, in_cart=True)
        plan_list = []
        plan_id_list = []
        total = 0

        for sub in subs:
            plan_list += [sub.plan_id]
            plan_id_list += [{"id": sub.id}]
            total += sub.plan_id.price

        form_link = os.getenv('PAY_FORM_LINK')

        data = {'cart': cart, 'plans': plan_list, 'form_link': form_link, 'total': total, 'cart_info': {"user": cart.user_id.id, "plans": plan_id_list},'form': form}
    else:
        data = {'message': "Nothing in your cart"}

    return render(request, 'cart/cart.html', data)
    # else:
    #
    #     return render(request, 'cart/cart.html', {'message': "Please bring your payments up to date to add a new plan"})

def add_coupon_code(request, cart_id):
    if request.method == 'POST':
        cart = Cart.objects.get(id=cart_id)
        form = CartCouponForm(request.POST)
        if form.is_valid():
            coupon = Coupon.objects.filter(code=form.cleaned_data('coupon_code'))
            if len(coupon) > 0:
                cart.price -= coupon.discount
                cart.save()
                form.save()


def webhook_success(request):
    if request.method == 'POST':
        print('hello')
        print(request.body)

        return HttpResponse('valid', status=200)
    else:
        print(request.GET.get('UMdescription'))
        decoded_des = urllib.parse.unquote(request.GET.get("UMdescription"))
        replaced_des = decoded_des.replace("'", '"')
        print(replaced_des)
        user_des = ''
        try:
            user_des = json.loads(replaced_des)
        except json.JSONDecodeError as e:
            print("JSON decoding error", e)
        print(f"user_des {user_des}")
        user = CustomUser.objects.get(id=int(user_des['user']))
        subs = user_des['plans']
        print(subs)
        for sub in subs:
            print(sub['id'])
            new_sub = Subscription.objects.get(id=sub['id'])
            new_sub.activation_date = datetime.now()
            new_sub.has_paid = True
            new_sub.save()
        print(user)
        billed = Billing(user_id=user, amount=request.GET.get('UMamount'), date_of_payment=datetime.now())

        user.latest_payment = datetime.now()
        user.save()
        billed.save()
        cart = Cart.objects.get(user_id=user.id)

        cart.delete()

        print(request.GET.get('UMamount'))
        return redirect('user_page')

def webhook_fail(request):
    return redirect('cart')

def webhook_response(request):
    print(request)
    return HttpResponse('valid', status=200)


# def checkout(request):
#     if request.method == "POST":
#         amount = 10
#         form = PaymentProfileForm(request.POST)
#         if form.is_valid():
#             charge_cc(amount, form.cleaned_data)
#             return redirect('user_page')
#
#     else:
#         form = PaymentProfileForm()
#         return render(request)


