# Generated by Django 4.1.7 on 2023-06-08 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='description',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
