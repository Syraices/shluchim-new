from django.contrib import admin

from .models import Subscription


# Register your models here.


# class SubPlotInline(admin.TabularInline):
#     model = SubPlan
#     raw_id_fields = ['sub_id']

class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscription
    fields = ['user_id', 'plan_id', 'is_active', 'imei', 'auto_sub', 'esim', 'esim_number', 'amount_owed', 'is_cancelled', 'activation_date', 'ban_account', 'has_paid', 'phone_number', 'is_suspended']
    list_display = ['id', 'user_id', 'is_active', 'created_at']
    readonly_fields = ['created_at']


admin.site.register(Subscription, SubscriptionAdmin)

# admin.site.register(SubPlan, SubPlanAdmin)
