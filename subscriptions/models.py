from django.db import models

from plans.models import Plan
from accounts.models import CustomUser


# Create your models here.
class Subscription(models.Model):
    plan_id = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)
    auto_sub = models.BooleanField(default=False)
    esim = models.BooleanField(default=True)
    imei = models.CharField(max_length=16, default=None)
    esim_number = models.CharField(max_length=25, default=None)
    amount_owed = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=15, default=None, null=True)
    # is_billing = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.user_id}: {self.plan_id} - {self.plan_id}"
