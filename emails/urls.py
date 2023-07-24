from django.urls import path

from . import views 


urlpatterns = [
    # path("<int:id>", views.send_email, name="send_email"),
    path('send_email/<int:email_id>', views.send_email, name='send_email'),
    # path('email_window/<int:id>', views.email_send_page, name='email_window')
]