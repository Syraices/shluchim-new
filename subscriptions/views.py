from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .forms import SubscriptionForm
from accounts.forms import CustomUserForm
from django.http import HttpRequest
from django.conf import settings
from .models import SubPlan
from plans.models import Plan
from accounts.models import CustomUser
from cart.models import Cart
import usaepay
from .models import Subscription


# from django_project.settings import USAEPAY_PIN, USAEPAY_SOURCE_KEY

# usaepay.api.set_authentication('_92vEyY940q7x62fI202uza63HK84qWU', '1770')

def create_subscription(request, plan_id):
    print(request.method)
    plan = Plan.objects.get(id=plan_id)
    # cart = Cart.objects.get(id=cart_id)
    # plans = cart.plan_ids.all()
    # print(plan)
    # plan = plans[0]

    usaepay.api.set_subdomain("sandbox")
    usaepay.api.set_authentication('_92vEyY940q7x62fI202uza63HK84qWU', '1770')
    if request.method == 'POST':
        form_sub = SubscriptionForm(request.POST)
        form_user = CustomUserForm(request.POST)

        data = form_sub.data.copy()

        if form_user.is_valid():

            user_id = form_user.save()
            user_id = user_id.pk

            user_info = CustomUser.objects.get(id=user_id)

            data['user_id'] = user_info
            data['plan_id'] = [Plan.objects.get(id=plan_id)]
            print('line 53')
            # print(form_sub.data.get('plan_id'))
            print(data['plan_id'])
            # print(data)

            new_form = SubscriptionForm(data)
            # print('line 50')
            # print(new_form.data.get('plan_id'))
            # print(new_form.errors)

            cart = None
            if new_form.is_valid():
                # print("form_sub worked")
                # print("cleaned")
                #
                # print(new_form.cleaned_data)
                # print(new_form.cleaned_data['plan_id'])

                new_form_res = new_form.save()
                # print(new_form_res)
                plan_list = []
                plans_price = 0
                for plan_id in data['plan_id']:
                    plan_list += [plan_id]
                    plans_price += plan_id.price

                cart = Cart(user_id=user_info, price=plans_price)
                print(cart.user_id)
                # print(plan_list[0].name)
                cart.full_clean()
                print(cart)
                cart_id = cart.save()
                print(cart_id)

                cart.plan_ids.set(plan_list)
                print(cart.plan_ids)

                # pay_request = {
                #     "command": "sale",
                #     "amount": "500.00",
                #     "creditcard": {
                #         "cardholder": "me",
                #         "number": "4000100011112224",
                #         "expiration": "0924",
                #         "cvc": "123"
                #     },
                #     "billing_address": {
                #         "firstname": "John",
                #         "lastname": "Doe",
                #         "street": "123 Astronomy Tower",
                #         "city": "ywhoopitz",
                #         "state": "MD",
                #         "postalcode": "21215",
                #         "country": "USA",
                #         "phone": "1234567890",
                #     },
                #     "shipping_address": {
                #         "firstname": "John",
                #         "lastname": "Doe",
                #         "street": "123 Astronomy Tower",
                #         "city": "ywhoopitz",
                #         "state": "MD",
                #         "postalcode": "21215",
                #         "country": "USA",
                #         "phone": "1234567890",
                #     },
                #     "lineitems": {
                #         "name": f"{plan.name}",
                #         "cost": f"{plan.price}",
                #         "qty": "1"
                #     }
                #
                # }
                #
                # pay_response = usaepay.transactions.post(pay_request)
                # print("Response")
                # print(pay_response)

            return redirect('cart', cart_id=cart.id)

        else:

            print('invalid')
            print(form_sub.errors)
    else:
        form_sub = SubscriptionForm()
        form_sub.fields['plan_id'].initial = [plan]
        # form_sub.fields['user_id'].initial = 5000000
        form_sub.fields['amount_owed'].initial = plan.price
        print('Now this is the way we go')
        print('line 118')
        # print(list(form_sub.fields['plan_id'].choices))
        form_user = CustomUserForm()

    # print(request)

    return render(request, 'subscriptions/subscribe.html', {'form_sub': form_sub, 'form_user': form_user, 'plan': plan})
