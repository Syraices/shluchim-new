from django import forms

from .models import Cart


class CartCreateForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = [ 'user_id']
        # widget = {
        #     'plan_ids': forms.HiddenInput(),
        # }

class CartCouponForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['coupon_codes']