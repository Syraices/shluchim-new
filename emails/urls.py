from django.urls import path

from . import views 


urlpatterns = [
    # path("<int:id>", views.send_email, name="send_email"),
    path('send_email/<int:id>', views.send_email, name='send_email'),

]