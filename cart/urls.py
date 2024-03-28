from django.urls import path

from . import views

urlpatterns = [
    path("", views.cart, name="cart"),
    path("subbed", views.webhook_success, name="cart_subbed"),
    path("unsubbed", views.webhook_fail, name="cart_unsubbed"),
    path("web_res", views.webhook_response, name="cart_res"),
    path("coupon_code/<int:cart_id>", views.add_coupon_code, name="cart_code"),
]
