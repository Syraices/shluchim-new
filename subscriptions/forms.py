from django import forms

from .models import Subscription
from accounts.models import CustomUser
from plans.models import Plan


class SubscriptionForm(forms.ModelForm):
    plan_id = forms.ModelChoiceField(required=False, widget=forms.HiddenInput(), queryset=Plan.objects.all())
    user_id = forms.ModelChoiceField(required=False, widget=forms.HiddenInput(), queryset=CustomUser.objects.all())

    class Meta:
        model = Subscription
        fields = ('plan_id', 'user_id', 'esim', 'esim_number', 'imei', 'phone_number', 'amount_owed')
        labels = {
            'esim': 'Check box if you already have an esim',
            'phone_number': 'If you would like to use your old number, enter it here',
            'esim_number': 'eSIM',
            'imei': 'IMEI',
            'plan_id': 'Confirm your plan'
        }
        widgets = {
            'esim': forms.CheckboxInput(attrs={'id': 'esim-check'}),
            'esim_number': forms.TextInput(attrs={'id': 'esim-number'}),
            # 'user_id': forms.HiddenInput(attrs={'required': False}),
            'amount_owed': forms.HiddenInput()
        }


class SubscriptionAddForm(forms.ModelForm):
    user_id = forms.ModelChoiceField(required=False, widget=forms.HiddenInput(), queryset=CustomUser.objects.all())
    class Meta:
        model = Subscription
        fields = ('user_id', 'plan_id', 'esim', 'esim_number', 'imei', 'phone_number', 'amount_owed')
        labels = {
            'esim': 'Check box if you already have an esim',
            'phone_number': 'If you would like to use your old number, enter it here',
            'esim_number': 'eSIM',
            'imei': 'IMEI',
            'plan_id': 'Choose plan'
        }
        widgets = {
            'esim': forms.CheckboxInput(attrs={'id': 'esim-check'}),
            'esim_number': forms.TextInput(attrs={'id': 'esim-number'}),
            # 'user_id': forms.HiddenInput(attrs={'required': False}),
            'amount_owed': forms.HiddenInput()
        }

class SubscriptionActivateForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ('phone_number', 'ban_account')

    # def save(self):
    #     pass
