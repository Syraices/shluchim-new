# Generated by Django 4.1.7 on 2023-04-19 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0003_rename_plans_plan'),
        ('accounts', '0003_customuser_plan_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='plan_id',
        ),
        migrations.AddField(
            model_name='customuser',
            name='plan_id',
            field=models.ManyToManyField(null=True, to='plans.plan'),
        ),
    ]
