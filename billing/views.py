from django.http import HttpResponse
from django.shortcuts import render, redirect

from accounts.models import CustomUser
from .models import Billing, paymentProfile
from utils import delete_pay, add_pay, recurring_pay, charge_existing_customer, charge_cc, create_customer_profile, \
    send_custom_email
from .forms import PaymentProfileForm
from subscriptions.models import Subscription
# Create your views here.
# def payment_webhook(request, key):

def index(request):
    billing_list = Billing.objects.find(user_id=request.user)
    if len(billing_list) > 0:

        return render(request, 'billing/billing_main.html', {'billings': billing_list})
    else:
        return "No billin yet"




def delete_pay_method(request, payment_profile):
    if request.method == 'POST':
        delete_pay(request.user.authnet_id, str(payment_profile))
        pay_profile = paymentProfile.objects.get(profile_number=payment_profile)
        pay_profile.delete()

        return redirect('user_page')

def add_pay_method(request):
    if request.method == 'POST':
        form = PaymentProfileForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['recurring']:
                response = recurring_pay(1.00, form.cleaned_data)
            else:
                response = add_pay(request.user.authnet_id, form.cleaned_data)
        return redirect('user_page')


def single_charge(request, user_id, payment_profile):
    if request.user.is_superuser:
        if request.method == 'POST':
            amount = request.POST.get('amount')
            user = CustomUser.objects.get(id=user_id)
            response = charge_existing_customer(user.authnet_id, str(payment_profile), amount)
            print(response)
    return redirect('admin_user_page', user_id=user_id)


def checkout(request, amount=None):
    if request.method == "POST":
        form = PaymentProfileForm(request.POST)
        response = None
        if form.is_valid():
            if form.cleaned_data["save_payment"]:
                if not request.user.authnet_id:
                    response = create_customer_profile(str(request.user.id), form.cleaned_data)
                    print("response")
                    print(response)
                    response = charge_existing_customer(str(request.user.authnet_id), str(response.payment_profile), amount)
                else:
                    pay_response = add_pay(str(request.user.authnet_id), form.cleaned_data)
                    response = charge_existing_customer(str(request.user.authnet_id), str(pay_response), amount)
                    print(pay_response)
                    print(response)
                    print("saved")
            else:
                response = charge_cc(amount, form.cleaned_data)

            if response:
                subs = Subscription.objects.filter(user_id=request.user.id, in_cart=True)
                for sub in subs:
                    sub.in_cart = False
                    sub.is_active = True
                    sub.save()

                subject = "Your new plan"
                email_message = f"We've got your order and you're looking a whole lot more connected. We wanted to let you know that we offer three convenient options to get started with our service: E-SIM Activation: Our plan can now be used with E-SIM if your phone is compatible. You can check if your phone is E-SIM compatible by going to settings > about > status > EID. If your phone has an EID, then it's E-SIM compatible. If you'd like us to move your line onto your E-SIM, simply send us your IMEI and EID. Pickup: We offer a pickup option in Crown Heights that is available 24/7. If this option is more convenient for you, please let us know, and we'll provide you with the pickup location. Shipping: Our estimated shipping time is 3-7 business days. If you prefer to have your order shipped to you, we'll send it out promptly. Please let us know which option you prefer, and we'll take care of the rest. Thanks again for choosing our services. If you have any questions, please don't hesitate to reach out to us.Thank you for choosing Shluchim Assist, have a great day!"

                context = {
                    "recipient_name": request.user.ship_fname,
                    'email_message': email_message
                }

                print('67')
                send_custom_email(request.user.email, subject, 'email_template.html', context, request.user)

                return redirect('user_page')
            else:
                return HttpResponse("your payment did not go through", status=400)
    else:
        form = PaymentProfileForm()
        return render(request, "billing/checkout.html", {"form": form, "amount": amount})