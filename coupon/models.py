from django.db import models
from django.utils import timezone

from accounts.models import CustomUser


# Create your models here.
class Coupon(models.Model):
    name = models.CharField(max_length=20, unique=True, null=True)
    code = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.code

class CouponUsage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    used_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.coupon}"
