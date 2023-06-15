from django.db import models

from plans.models import Plan
from accounts.models import CustomUser


class Billing(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    plan_id = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField()
    date_of_payment = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.user_id}: {self.plan_id} - {self.plan_id}"
