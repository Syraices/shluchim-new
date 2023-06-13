from django.urls import path

from . import views 

urlpatterns = [
    path("", views.index),
    path("change_plan", views.change_plan, name='change_plan'),
    path("<slug:slug>", views.plan, name='plan_detail'),
   
]
