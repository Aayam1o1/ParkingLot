# Generated by Django 5.0.6 on 2024-07-10 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0017_alter_parkingdetail_vehicle_arrived_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="parkingdetail",
            name="vehicle_left_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
