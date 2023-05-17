from django.contrib import admin

from .models import Email
from .forms import EmailForm

# Register your models here.
class EmailAdmin(admin.ModelAdmin):
    model = Email
    fields = ['name', 'subject_line', 'email_content']

    form = EmailForm


admin.site.register(Email, EmailAdmin)