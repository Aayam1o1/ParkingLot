# Generated by Django 5.0.6 on 2024-07-10 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "core",
            "0013_rename_car_arrived_date_parkingdetail_vehicle_arrived_date_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="parkingdetail",
            name="vehicle_left_date",
        ),
    ]
