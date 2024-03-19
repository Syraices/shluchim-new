from django import forms
from django.core.validators import RegexValidator

from .models import Port

class CreatePortForm(forms.ModelForm):
    class Meta:
        model = Port
        fields = [
            'authorizedName',
            'port_number',
            'sim_number',
            'phone_company',
            'former_account',
            'account_pin',
            'address',
            'city',
            'state',
            'zip_code',
            'ssn_tax'
        ]