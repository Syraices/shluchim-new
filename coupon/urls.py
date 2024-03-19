from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='coupons'),
    path('add_coupon', views.add_coupon, name='add_coupon')
]