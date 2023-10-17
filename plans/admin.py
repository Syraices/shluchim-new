from django.contrib import admin

from .models import Plan, BanAccount


class PlanAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]


admin.site.register(Plan, PlanAdmin)


class BanAccountAdmin(admin.ModelAdmin):
    fields = None


# Register your models here.
admin.site.register(BanAccount, BanAccountAdmin)
