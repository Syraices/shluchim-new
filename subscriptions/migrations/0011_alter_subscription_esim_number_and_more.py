# Generated by Django 4.1.7 on 2023-08-03 17:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0010_alter_subscription_esim_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='esim_number',
            field=models.CharField(default=None, max_length=25, unique=True, validators=[django.core.validators.MaxLengthValidator(25)]),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='imei',
            field=models.CharField(default=None, max_length=16, null=True, unique=True, validators=[django.core.validators.MaxLengthValidator(16)]),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='phone_number',
            field=models.CharField(default=None, max_length=10, null=True, unique=True, validators=[django.core.validators.MaxLengthValidator(10)]),
        ),
    ]