from django import forms
from django.core.validators import RegexValidator


class PaymentProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    address = forms.CharField(max_length=30, required=True)
    city = forms.CharField(max_length=30, required=True)
    state = forms.CharField(max_length=2, required=True)
    zip = forms.CharField(max_length=5, required=True)
    card_number = forms.CharField(max_length=16, required=True)
    expiration_date = forms.CharField(max_length=4, required=True)
    cvc = forms.CharField(max_length=3, required=True)
    default_card = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    recurring = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    save_payment = forms.BooleanField(required=False, widget=forms.CheckboxInput())
