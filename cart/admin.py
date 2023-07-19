from django.contrib import admin

# Register your models here.
from .models import Cart
# Register your models here.


class CartAdmin(admin.ModelAdmin):
    model = Cart
    fields = ['plan_ids', 'price', 'user_id']


admin.site.register(Cart, CartAdmin)