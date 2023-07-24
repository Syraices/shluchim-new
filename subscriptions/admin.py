from django.contrib import admin

from .models import Subscription


# Register your models here.


# class SubPlotInline(admin.TabularInline):
#     model = SubPlan
#     raw_id_fields = ['sub_id']

class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscription
    fields = ['user_id', 'is_active', 'imei', 'auto_sub', 'esim', 'esim_number', 'amount_owed']
    # filter_vertical = ('plan_id',)
    # inlines = [SubPlotInline]


# class SubPlanAdmin(admin.ModelAdmin):
#     filter_horizontal = ('plan_id',)


admin.site.register(Subscription, SubscriptionAdmin)

# admin.site.register(SubPlan, SubPlanAdmin)
