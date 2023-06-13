from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.urls import reverse

from .models import Email
from accounts.models import CustomUser

# Create your views here.
def send_email(request, id):
    email = Email.objects.get(id=id)
    users = CustomUser.objects.all()

    print(id)
    if request.method == "GET":
        details = {'users': users, 'email': email, 'id': id}
        return render(request, 'emails/send_email.html', details)
    if request.method == 'POST':
        print(id)
        selected_option = request.POST['user_email']
        user = CustomUser.objects.get(email=selected_option)
        email_content = email.email_content.replace("[fname]", user.ship_name)
        send_mail(
                email.subject_line,
                email_content,
                'rdevcotest@gmail.com',
                [selected_option],
                fail_silently=False,
            )
            
        return redirect('/admin')
    # print("not post")
    return redirect('/admin')

# def email_send_page(request, id):
#     email = Email.objects.id

#     return 

