from django.urls import path

from . import views 

urlpatterns = [
    path("", views.index, name="billing_main"),
    path("delete/<int:payment_profile>", views.delete_pay_method, name="delete_pay"),
    path("add", views.add_pay_method, name="add_pay"),
    path("single/<int:user_id>/<int:payment_profile>", views.single_charge, name="single_charge"),
    path("checkout/<int:amount>", views.checkout, name="checkout")
]
