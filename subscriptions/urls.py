from django.urls import path

from . import views 


urlpatterns = [
    path("<int:plan_id>", views.create_subscription, name='subscribe'),
    path("add-plan/<int:cart_id>", views.add_plan, name='add_plan'),
]