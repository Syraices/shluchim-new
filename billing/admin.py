from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Billing
# Register your models here.


class BillingAdmin(admin.ModelAdmin):
    model = Billing
    fields = ['user_id', 'plan_id', 'amount', 'date_of_payment']


admin.site.register(Billing, BillingAdmin)