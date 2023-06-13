from django.contrib import admin

from .models import Subscription
# Register your models here.


class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscription
    fields = ['plan_id', 'user_id', 'is_active', 'imei', 'auto_sub', 'esim', 'esim_number']


admin.site.register(Subscription, SubscriptionAdmin)