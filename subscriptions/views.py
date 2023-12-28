import smtplib

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.utils import timezone

from emails.models import EmailRecords
from .forms import SubscriptionForm, SubscriptionAddForm
from accounts.forms import CustomUserForm
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound

from plans.models import Plan, BanAccount
from accounts.models import CustomUser
from cart.models import Cart
from .models import Subscription
from django.core.mail import send_mail


def create_subscription(request, plan_id):
    print(request.method)
    print("got to this point")
    plan = Plan.objects.get(id=plan_id)

    if request.method == 'POST':
        form_sub = SubscriptionForm(request.POST)
        form_user = CustomUserForm(request.POST)
        print("GOt the forms")
        data = form_sub.data.copy()

        if form_user.is_valid():

            user_id = form_user.save()

            user_id = user_id.pk
            print("saved user")
            user_info = CustomUser.objects.get(id=user_id)

            data['user_id'] = user_info
            data['plan_id'] = plan
            print('line 53')
            print(data['plan_id'])

            new_form = SubscriptionForm(data)
            print(new_form.data.get('plan_id'))
            print(new_form.errors)

            cart = None
            if new_form.is_valid():
                new_form_res = new_form.save()
                print("saved sub")

                cart = Cart(user_id=user_info, price=plan.price)

                cart.full_clean()
                print('cart')
                print(cart)
                cart_id = cart.save()

                print(cart)

                return redirect('cart')

        else:

            print('invalid')
            print(form_sub.errors)
            return HttpResponseNotFound("No cart was created")

    else:
        form_sub = SubscriptionForm()
        form_sub.fields['plan_id'].initial = plan
        form_sub.fields['amount_owed'].initial = plan.price
        print('Now this is the way we go')
        print('line 118')
        form_user = CustomUserForm()

    return render(request, 'subscriptions/subscribe.html', {'form_sub': form_sub, 'form_user': form_user, 'plan': plan})


def add_plan(request):
    fail_message = None
    cart = None
    if request.user:
        try:
            cart = Cart.objects.get(user_id=request.user.id)
        except Exception as e:
            cart = Cart(user_id=request.user)
            cart.save()
        if request.method == 'POST':
            form = SubscriptionAddForm(request.POST)
            print(form.errors)
            if form.is_valid():
                form.cleaned_data['amount_owed'] = form.cleaned_data['plan_id'].price

                print(form.cleaned_data['amount_owed'])
                print(form.cleaned_data['user_id'])

                saved_form = form.save()

                print(saved_form)
                return redirect('cart')

            else:
                fail_message = 'oops something went wrong, please try again'
                return redirect('add_plan')
        else:
            print(request.user)
            form = SubscriptionAddForm()
            form.fields['amount_owed'].initial = 1
            form.fields['user_id'].initial = request.user

            return render(request, 'subscriptions/add_sub.html', {'form': form, 'message': fail_message})


def delete_plan(request, sub_id):
    print(request.method)
    if request.method == 'POST':
        if request.user.is_superuser:
            sub = Subscription.objects.get(id=sub_id)
            print(sub.is_cancelled)
            sub.is_cancelled = True
            sub.is_active = False
            sub.save()
            print(sub.is_cancelled)
            return redirect('admin_user_page', user_id=sub.user_id.id)
        else:
            subject = 'Cancellation Request'
            message = f'{request.user.ship_fname} {request.user.ship_lname} has requested a cancellation'
            print(request.user.email)
            try:
                sent_email = send_mail(
                    subject,
                    message,
                    'rdevcotest@gmail.com',
                    ['bigmouth28@gmail.com'],
                    fail_silently=True
                )
                email_record = EmailRecords(user_id=request.user, subject=subject, content=message)
                email_record.save()
                print(email_record)
                print("send email to admin")
            except smtplib.SMTPException as e:
                print('exception')
                print(e)
            return render(request, 'subscriptions/delete_success.html')
    else:
        return render(request, 'subscriptions/delete_plan.html', {'sub_id': sub_id})

def admin_user(request, user_id):
    subs = Subscription.objects.filter(user_id=user_id)

    return render(request, 'subscriptions/admin_user.html',{'subs': subs})

def activate_plan(request, sub_id):
    print("This is the sub id", sub_id)
    print(request.POST.get('ban_account').split(': '))

    phone_number = request.POST.get('phone_number')
    ban_account = request.POST.get('ban_account').split(': ')
    sub = Subscription.objects.get(id=sub_id)
    if request.method == 'GET':
        sub = Subscription.objects.get(id=sub_id)
        return render(request, 'subscriptions/activate.html', {'sub': sub})
    elif request.method == 'POST':
        sub.is_active = True
        sub.activation_date = timezone.now()
        sub.phone_number = phone_number
        sub.ban_account = BanAccount.objects.get(ban_number=ban_account[1])
        sub.save()
        return redirect("actions_queue")


def deactivate_plan(request, sub_id):
    sub = Subscription.objects.get(id=sub_id)
    if request.method == 'GET':
        return HttpResponseNotFound('<h1>Resource not found</h1>')
    elif request.method == 'POST':
        # sub.is_active = False
        sub.is_suspended = True
        sub.save()
        return redirect("actions_queue")


