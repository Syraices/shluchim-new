from django import forms
from .models import Coupon

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['name', 'code', 'discount']


class UserCouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code']
