# Generated by Django 4.1.7 on 2023-12-28 04:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_emailrecords'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailrecords',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]