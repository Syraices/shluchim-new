from django.contrib import admin
from .models import Port
# Register your models here.

class PortAdmin(admin.ModelAdmin):
    model = Port


admin.site.register(Port, PortAdmin)


