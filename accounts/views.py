from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from allauth.account.decorators import verified_email_required

from .models import CustomUser 
from plans.models import Plan

# Create your views here.
def dispatch(self, request):
    print(request)
    return super(self).dispatch(request)

@login_required
# @verified_email_required
def user_page(request, id):
    # print(request.user.plan_id.name)
    # print(request.user.plan_id.color)

    if request.user.id == id:
        user = request.user
        plans = user.plan_id.all()
        user_details = {'user': user, 'plans': plans}
        for plan in plans:
            print(plan)
        print(plans)

        return render(request, 'accounts/user_page.html', user_details)
    else:
        return render(request, '404.html')



