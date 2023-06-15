from django.shortcuts import render, redirect
from .forms import SubscriptionForm
from django.http import HttpRequest

from plans.models import Plan


# from django_project.settings import USAEPAY_PIN, USAEPAY_SOURCE_KEY

# usaepay.api.set_authentication('_wh3eJ1Uf0QCydt2z5534X1UDsojDGv4', '1770')

def create_subscription(request, plan_id):
    print(request.method)
    plan = Plan.objects.get(id=plan_id)

    # usaepay.api.set_authentication("_wh3eJ1Uf0QCydt2z5534X1UDsojDGv4", "1770")
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            # print(form)
            form.save()
            print(form)
            return redirect('user_page')

        else:
            print('invalid')

    else:
        form = SubscriptionForm()
        form.fields['plan_id'].initial = plan_id
        form.fields['user_id'].initial = request.user.id
        form.fields['amount_owed'].initial = plan.price
        print('Now this is the way we go')
        print(form.fields)
    # print(request)
    return render(request, 'subscriptions/subscribe.html', {'form': form})

    # pay_request = {
    #     "command": "sale",
    #     "amount": "500.00",
    #     "creditcard": {
    #         "cardholder": "me",
    #         "number": "4000100011112224",
    #         "expiration": "0924",
    #         "cvc": "123"
    #         },
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
    #          "firstname": "John",
    #         "lastname": "Doe",
    #         "street": "123 Astronomy Tower",
    #         "city": "ywhoopitz",
    #         "state": "MD",
    #         "postalcode": "21215",
    #         "country": "USA",
    #         "phone": "1234567890",
    #     },
    #     "lineitems": {
    #         "name": "plan",
    #         "cost": "500.00",
    #         "qty": "1"
    #     }
    #
    # }

    # pay_response = usaepay.Transactions(pay_request)
    #
    # print(pay_response)
