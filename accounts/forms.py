from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserForm(UserCreationForm):
     class Meta:
        model = CustomUser
        fields = ('plan_id', 'username', 'email', 'phone_number', 'four_pin', 'ship_name')
        widgets = {
            'plan_id': forms.HiddenInput(),
        }



    
