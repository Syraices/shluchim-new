import smtplib

from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.urls import reverse
from .forms import SingleEmailForm

from .models import Email, EmailRecords
from accounts.models import CustomUser


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
                email_sent = send_mail(
                    subject,
                    message,
                    'rdevcotest@gmail.com',
                    [recipient_email],
                    fail_silently=False,
                )
                email_record = EmailRecords(user_id=user_email, subject=subject, content=message)
                email_record.save()
                print("no exception")
                print(email_sent)
            except smtplib.SMTPException as e:
                print('exception')
                print(e)
            return redirect(f'/my-account/{email_id}')
    # print("not post")
    else:
        form = SingleEmailForm()

        return render(request, 'emails/single_email.html', {'form': form})
    return redirect(f'/my-account/{email_id}')

# def email_send_page(request, id):
#     email = Email.objects.id

#     return
