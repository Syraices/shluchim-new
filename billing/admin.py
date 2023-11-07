from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Billing


# Register your models here.


class BillingAdmin(admin.ModelAdmin):
    model = Billing
    fields = ['user_id', 'amount', 'date_of_payment']
    list_display = ['get_billing_id']

    def get_billing_id(self, obj):
        return obj.subscription.id

admin.site.register(Billing, BillingAdmin)
