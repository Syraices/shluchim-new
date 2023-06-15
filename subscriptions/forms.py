from django import forms

from .models import Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ('plan_id', 'user_id', 'esim', 'esim_number', 'imei', 'phone_number', 'amount_owed')
        labels = {
            'esim': 'Check box if you already have an esim',
            'phone_number': 'If you would like to use your old number, enter it here',
            'esim_number': 'eSIM',
            'imei': 'IMEI'
        }
        widgets = {
            'esim': forms.CheckboxInput(attrs={'id': 'esim-check'}),
            'esim_number': forms.TextInput(attrs={'id': 'esim-number'}),
            'plan_id': forms.HiddenInput(),
            'user_id': forms.HiddenInput(),
            'amount_owed': forms.HiddenInput()
        }

    def save(self):
        pass
