from django.db import models

from subscriptions.models import Subscription
from plans.models import Plan
from accounts.models import CustomUser


# Create your models here.

class Cart(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField(null=True, default=None)

    def __str__(self) -> str:
        return f"{self.price}"

