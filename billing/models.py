from django.db import models

from plans.models import Plan
from accounts.models import CustomUser
from subscriptions.models import Subscription


class Billing(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField(default=0)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    date_of_payment = models.DateTimeField(default=None, null=True)
    pass

    def __str__(self) -> str:
        return f"{self.user_id}, {self.date_of_payment}, {self.subscription}"

class paymentProfile(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    profile_number = models.CharField(max_length=25, null=False)

