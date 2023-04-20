from django.contrib import admin

from .models import Plan


class PlanAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]

# Register your models here.
admin.site.register(Plan, PlanAdmin)