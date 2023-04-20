# Generated by Django 4.1.7 on 2023-04-18 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0003_rename_plans_plan'),
        ('accounts', '0002_customuser_four_pin_customuser_phone_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='plan_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='plans.plan'),
        ),
    ]
