# Generated by Django 4.1.7 on 2023-07-19 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0002_plan_description'),
        ('subscriptions', '0003_alter_subscription_plan_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='plan_id',
        ),
        migrations.DeleteModel(
            name='SubPlan',
        ),
        migrations.AddField(
            model_name='subscription',
            name='plan_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='plans.plan'),
        ),
    ]