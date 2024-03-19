from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_cryptography.fields import encrypt

from accounts.models import CustomUser
from plans.models import BanAccount
from subscriptions.models import Subscription


# Create your models here.
class Port(models.Model):
    sub_id = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True )
    authorizedName = models.CharField(max_length=30, null=False)
    port_number = models.CharField(max_length=10, null=False)
    sim_number = models.CharField(max_length=25,null=False)
    phone_company = models.CharField(max_length=25, null=False)
    account_pin = models.CharField(max_length=6, null=False)
    name = models.CharField(max_length=50, default='john doe')
    address = models.CharField(max_length=50, default="asd st")
    city = models.CharField(max_length=20, default='test')
    state = models.CharField(max_length=2, default='md')
    zip_code = models.CharField(max_length=5, default='21215')
    ssn_tax = encrypt(models.CharField(max_length=9, default='000000000'))
    former_account = encrypt(models.CharField(max_length=25, default='12121212121212'))
