# Generated by Django 5.0.6 on 2024-07-10 06:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0014_remove_parkingdetail_vehicle_left_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="parkingdetail",
            name="vehicle_has_left",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="parkingdetail",
            name="vehicle_left_date",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
