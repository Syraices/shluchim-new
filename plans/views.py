from django.shortcuts import render
from django.http import HttpResponse 
from django.template.loader import render_to_string
from django.urls import reverse
from .models import Plan

def index(request):
    plans = Plan.objects.all()
    plan_list = {'plans': plans}
    response_data = render_to_string("plans/plans.html", plan_list)
    return HttpResponse(response_data)

def plan(request, slug):
    plan = Plan.objects.get(slug=slug)
    print(request)
    plan_details = {'plan': plan}
    response_data = render_to_string("plans/plan.html", plan_details)
    return HttpResponse(response_data)

def change_plan(request):
    print(request.user)
    plans = Plan.objects.all()
    plan_list = {'plans': plans, 'id': request.user.id}
    response_data = render_to_string("plans/change_plan.html", plan_list)

    return HttpResponse(response_data)