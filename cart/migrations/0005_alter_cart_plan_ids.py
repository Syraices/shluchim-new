# Generated by Django 4.1.7 on 2023-07-18 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0002_plan_description'),
        ('cart', '0004_cart_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='plan_ids',
            field=models.ManyToManyField(blank=True, to='plans.plan'),
        ),
    ]
