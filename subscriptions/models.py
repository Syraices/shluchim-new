from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db import models

from plans.models import Plan, BanAccount
from accounts.models import CustomUser


def specific_length_validator(max_length):
    return MaxLengthValidator(max_length)

# Create your models here.
class Subscription(models.Model):
    plan_id = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    ban_account = models.ForeignKey(BanAccount, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False, null=True)
    auto_sub = models.BooleanField(default=False, null=True)
    esim = models.BooleanField(default=True, null=True)
    imei = models.CharField(max_length=16, validators=[specific_length_validator(16)], default=None, null=True, unique=True)
    esim_number = models.CharField(max_length=25, validators=[specific_length_validator(25)], default=None, unique=True)
    amount_owed = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=10, validators=[specific_length_validator(10)], default=None, null=True, unique=True)
    is_cancelled = models.BooleanField(default=False)
    has_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"{self.user_id}: {self.plan_id} - {self.plan_id}"



