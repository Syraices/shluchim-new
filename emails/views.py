import smtplib

from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.urls import reverse
from .forms import SingleEmailForm, EmailForm

from .models import Email, EmailRecords
from accounts.models import CustomUser
from utils import send_custom_email


# Create your views here.
def send_email(request, email_id):
    user_email = CustomUser.objects.get(id=email_id)

    if request.method == 'POST':
        form = SingleEmailForm(request.POST)

        if form.is_valid():
            recipient_email = user_email.email
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            try:
                context = {
                    'recipient_name': user_email.ship_fname,
                    'email_message': message
                }
                email_sent = send_custom_email(
                    rec_email=recipient_email,
                    subject=subject,
                    template_name='email_template.html',
                    context=context,
                    rec_id=user_email,
                )
                # email_record = EmailRecords(user_id=user_email, subject=subject, content=message)
                # email_record.save()
                print("no exception")
                print(email_sent)
            except smtplib.SMTPException as e:
                print('exception')
                print(e)
            return redirect(f'/my-account/{email_id}')
    # print("not post")
    else:
        form = SingleEmailForm()
        custom_form = EmailForm()

        return render(request, 'emails/user_email.html', {'form': form, 'custom_form': custom_form})
    return redirect(f'/my-account/{email_id}')

def email_template(request, user_id):
    print('email/view/email_tem[late')
    print(request.method)
    if request.method == 'POST':
        print('email/view/template')
        rec_user = CustomUser.objects.get(id=user_id)
        rec_email = rec_user.email
        print(rec_user)
        print(rec_email)
        subject = 'sndiuhfjbiwjbh'
        template_name = 'email_template.html'
        context = {
            'recipient_name': rec_user.ship_fname,
            'email_message': 'This is an email being sent to you for those that are funnies'
        }
        send_custom_email(rec_email, subject, template_name, context, rec_user)
        print('amil/view/email_template')
        return redirect('actions_queue')
    else:
        return render(request, 'emails/testing_template.html')

def send_email_templates(request, email_id, user_id):
    if request.user.is_superuser:
        if request.method == 'POST':
            rec_user = CustomUser.objects.get(id=user_id)
            canned_email = Email.objects.get(id=email_id)
            context = {
                'recipient_name': rec_user.ship_fname,
                'email_message': canned_email.email_content
            }
            sent_email = send_custom_email(rec_user.email, canned_email.subject_line, 'email_template.html', context, rec_user)
            print(sent_email)
            return redirect('actions_queue')


def add_email(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = EmailForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('actions_queue')


# def email_send_page(request, id):
#     email = Email.objects.id

#     return
