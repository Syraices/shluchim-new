# Generated by Django 4.1.7 on 2024-01-03 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0003_emailrecords_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='auto_emails',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='email',
            name='canned',
            field=models.BooleanField(default=False),
        ),
    ]