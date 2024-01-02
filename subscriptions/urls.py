from django.urls import path

from . import views 


urlpatterns = [
    path("<int:plan_id>", views.create_subscription, name='subscribe'),
    path("add-plan", views.add_plan, name='add_plan'),
    path("del-plan/<int:sub_id>", views.delete_plan, name='del_plan'),
    path("admin_user/<int:user_id>", views.admin_user, name="admin_user"),
    path("activate/<int:sub_id>", views.activate_plan, name="activate_user"),
    path("deactivate/<int:sub_id>", views.deactivate_plan, name="deactivate_user"),
    path("data-pass", views.data_pass, name='data_pass')
]