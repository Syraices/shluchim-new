from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.urls import reverse

from .models import Email

# Create your views here.
def send_email(request, id):
    email = Email.objects.get(id=id)
    print(email)
    if request.method == 'POST':
        print("post")
        send_mail(
                email.subject_line,
                email.email_content,
                'rdevcotest@gmail.com',
                ['bigmouth28@gmail.com'],
                fail_silently=False,
            )
        return redirect('/admin')
    print("not post")
    return redirect('/admin')