from django.urls import path

from . import views

urlpatterns = [
    path("", views.billing_alerts, name="billing_alerts"),

]
