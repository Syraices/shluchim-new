from django.contrib import admin
from .models import Coupon, CouponUsage
# Register your models here.
class CouponAdmin(admin.ModelAdmin):
    model = Coupon
    fields = ['name', 'code', 'discount', 'active']


admin.site.register(Coupon, CouponAdmin)


class CouponUsageAdmin(admin.ModelAdmin):
    model = CouponUsage
    fields = ['user', 'coupon']


admin.site.register(CouponUsage, CouponUsageAdmin)