import os

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from .models import Plan
from accounts.models import CustomUser
import os


def index(request):
    print(os.environ.get('NAME'))
    plans = Plan.objects.all()
    # print(plans)
    plan_list = {'plans': plans}
    response_data = render_to_string("plans/plans.html", plan_list, request=request)
    return HttpResponse(response_data)


def plan(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    plan_details = {'plan': plan}
    response_data = render_to_string("plans/plan.html", plan_details, request=request)
    return HttpResponse(response_data)


def change_plan(request):
    plans = Plan.objects.all()
    plan_list = {'plans': plans, 'id': request.user.id}
    response_data = render_to_string("plans/change_plan.html", plan_list, request=request)

    return HttpResponse(response_data)
