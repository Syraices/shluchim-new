from django.urls import path

from . import views 

urlpatterns = [
    path("", views.index, name='plan_choose'),
    path("change_plan", views.change_plan, name='change_plan'),
    path("<int:plan_id>", views.plan, name='plan_detail'),

]
