from django.contrib.auth.models import AbstractUser
from django.db import models
from plans.models import Plan


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=10, null=True)
    four_pin = models.CharField(max_length=4, null=True)
    # plan_id = models.ManyToManyField(Plan)
    ship_name = models.CharField(max_length=100, null=True)
    ship_address = models.CharField(max_length=100, null=True)
    ship_city = models.CharField(max_length=100, null=True)
    ship_state = models.CharField(max_length=2, null=True)
    ship_zip = models.CharField(max_length=5, null=True)
    is_billing = models.BooleanField(default=True)

    REQUIRED_FIELDS = ["phone_number", "four_pin", "ship_name", "ship_address", "ship_city", "ship_state", "ship_zip"]

    def __str__(self):
        return self.email
