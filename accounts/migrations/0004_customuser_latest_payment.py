# Generated by Django 4.1.7 on 2023-08-03 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_created_at_customuser_modified_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='latest_payment',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]