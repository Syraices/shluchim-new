from django.urls import path

from . import views 

urlpatterns = [
    path("<int:id>", views.user_page, name="user_page")
]
