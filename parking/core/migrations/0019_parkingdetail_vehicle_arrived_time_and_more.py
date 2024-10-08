# Generated by Django 5.0.6 on 2024-07-10 08:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0018_alter_parkingdetail_vehicle_left_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="parkingdetail",
            name="vehicle_arrived_time",
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="parkingdetail",
            name="vehicle_left_time",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="parkingdetail",
            name="vehicle_arrived_date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="parkingdetail",
            name="vehicle_left_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
