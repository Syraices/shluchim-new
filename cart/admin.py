from django.contrib import admin

# Register your models here.
from .models import Cart
# Register your models here.


class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ['id', 'price', 'user_id']
    fields = ['price', 'user_id']
    readonly_fields = ['id']


admin.site.register(Cart, CartAdmin)