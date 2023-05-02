from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = "/my-account/{id}"
        return path.format(id=request.user.id)
    
    def save_user(self, request, user, form):

        print(self)
        print(request) 
        print(user)
        print(form)