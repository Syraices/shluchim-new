from django.urls import path

from . import views

urlpatterns = [
    path("<int:cart_id>", views.cart, name="cart"),
    path("subbed", views.webhook_success, name="cart"),
]
