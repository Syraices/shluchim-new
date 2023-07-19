from django.urls import path

from . import views

urlpatterns = [
    path("<int:cart_id>", views.cart, name="cart"),
]
