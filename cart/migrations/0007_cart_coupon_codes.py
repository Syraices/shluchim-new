# Generated by Django 4.1.7 on 2024-01-17 20:35

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_remove_cart_plan_ids'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='coupon_codes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, null=True, size=None),
        ),
    ]
