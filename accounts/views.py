from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm
from allauth.account.decorators import verified_email_required
from django.core.mail import send_mail


from .models import CustomUser 
from plans.models import Plan
from .forms import CustomUserPlanChange

# Create your views here.
# def dispatch(self, request):
#     print(request)
#     return super(self).dispatch(request)

@login_required
# @verified_email_required
def user_page(request, id):
    # print(request.user.plan_id.name)
    # print(request.user.plan_id.color)

    if request.user.id == id:

        # send_mail(
        #     'Subject here',
        #     'Here is the message.',
        #     'syraices@gmail.com',
        #     ['bigmouth28@gmail.com'],
        #     fail_silently=False,
        # )
        user = request.user
        plans = user.plan_id.all()
        user_details = {'user': user, 'plans': plans}
        for plan in plans:
            print(plan)
        print(plans)

        return render(request, 'accounts/user_page.html', user_details)
    else:
        return render(request, '404.html')

def change_profile(request, user_id):
    if request.user.id == user_id:
        if request.method == 'POST':
            form = CustomUserPlanChange(request.POST)
            if form.is_valid():
                print(form)
                form.save()
                return redirect('user_page', id=user_id)
        else: 
            form = CustomUserPlanChange()
        print(request)
        return render(request, 'accounts/change_profile.html', {'form': form})
    else:
        return render(request, '404.html')