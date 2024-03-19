from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Billing, paymentProfile
from subscriptions.models import Subscription

# Register your models here.


class BillingAdmin(admin.ModelAdmin):
    model = Billing
    fields = ['user_id', 'amount', 'date_of_payment', 'subscription']
    list_display = ['get_billing_id', 'date_of_payment']

    def get_billing_id(self, obj):
        print("hello")
        print(obj)
        return obj.subscription.id if obj.subscription else None

admin.site.register(Billing, BillingAdmin)


class paymentProfileAdmin(admin.ModelAdmin):
    model = paymentProfile
    fields = ["user_id", "profile_number"]
    list_display = ['user_id', 'profile_number']

admin.site.register(paymentProfile, paymentProfileAdmin)
