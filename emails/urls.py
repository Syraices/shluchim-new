from django.urls import path

from . import views 


urlpatterns = [
    # path("<int:id>", views.send_email, name="send_email"),
    path('send_email/<int:email_id>', views.send_email, name='send_email'),
    path('add_email', views.add_email, name='add_email'),
    # path('email_window/<int:id>', views.email_send_page, name='email_window')
    path('test-template/<int:user_id>', views.email_template, name='send_test'),
    path('<int:email_id>/<int:user_id>', views.send_email_templates, name='canned_emails')
]