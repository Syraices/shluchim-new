from django import forms

from .models import Cart


class CartCreateForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['plan_ids', 'user_id']
        widget = {
            'plan_ids': forms.HiddenInput(),
        }

