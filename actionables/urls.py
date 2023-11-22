from django.urls import path

from . import views

urlpatterns = [
    # path("late", views.check_monthly_payments, name="past-due"),
    # path("activate", views.activation_queue, name="activate"),
    # path("sub_list", views.list_of_actives, name="sub_list"),
    path('actions', views.main_actions, name='actions_queue')
]
