from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from .models import Plan
from accounts.models import CustomUser


def index(request):
    # if request.user:
    #     user_person = CustomUser.objects.get(id=request.user.id)
    plans = Plan.objects.all()
    print(plans)
    plan_list = {'plans': plans}
    response_data = render_to_string("plans/plans.html", plan_list)
    return HttpResponse(response_data)


def plan(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    # print(request)
    plan_details = {'plan': plan}
    response_data = render_to_string("plans/plan.html", plan_details)
    return HttpResponse(response_data)


def change_plan(request):
    # print(request.user)
    plans = Plan.objects.all()
    plan_list = {'plans': plans, 'id': request.user.id}
    response_data = render_to_string("plans/change_plan.html", plan_list)

    return HttpResponse(response_data)
