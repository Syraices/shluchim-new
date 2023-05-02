from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['id', 'email', 'link_to_change_form', 'phone_number']
    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Personal Info', {'fields': ('email', 'ship_name', 'ship_address', 'phone_number')}),
        ('Plan', {'fields': ('plan_id',)})
    )
    def link_to_change_form(self, obj):
        url = reverse('admin:accounts_customuser_change', args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj.username)
        
    link_to_change_form.short_description = 'username (click to edit)'


admin.site.register(CustomUser, CustomUserAdmin)