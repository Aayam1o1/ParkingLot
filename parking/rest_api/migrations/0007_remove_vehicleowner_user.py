# Generated by Django 5.0.7 on 2024-07-23 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0006_alter_vehicleowner_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicleowner',
            name='user',
        ),
    ]
