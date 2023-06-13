from django.urls import path

from . import views 

urlpatterns = [
    path("", views.user_page, name="user_page"),
    path('change_profile/<int:user_id>', views.change_profile, name="change_profile")
]
