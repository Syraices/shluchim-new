# Generated by Django 4.1.7 on 2023-08-01 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0007_subscription_ban_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='has_paid',
            field=models.BooleanField(default=False),
        ),
    ]
