from django.shortcuts import render
# import usaepay

# from django_project.settings import USAEPAY_PIN, USAEPAY_SOURCE_KEY
# Create your views here.

# usaepay.api.set_authentication('_wh3eJ1Uf0QCydt2z5534X1UDsojDGv4', '1770')


def create_subscription(request):
    # usaepay.api.set_authentication("_wh3eJ1Uf0QCydt2z5534X1UDsojDGv4", "1770")


    pay_request = {
        "command": "sale",
        "amount": "500.00",
        "creditcard": {
            "cardholder": "me",
            "number": "4000100011112224",
            "expiration": "0924",
            "cvc": "123"
            },
        "billing_address": {
            "firstname": "John",
            "lastname": "Doe",
            "street": "123 Astronomy Tower",
            "city": "ywhoopitz",
            "state": "MD",
            "postalcode": "21215",
            "country": "USA",
            "phone": "1234567890",
        },
        "shipping_address": {
             "firstname": "John",
            "lastname": "Doe",
            "street": "123 Astronomy Tower",
            "city": "ywhoopitz",
            "state": "MD",
            "postalcode": "21215",
            "country": "USA",
            "phone": "1234567890",
        },
        "lineitems": {
            "name": "plan",
            "cost": "500.00",
            "qty": "1"
        }

    }
    
    # pay_response = usaepay.Transactions(pay_request)
    #
    # print(pay_response)


