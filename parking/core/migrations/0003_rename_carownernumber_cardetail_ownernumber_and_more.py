# Generated by Django 5.0.6 on 2024-07-09 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_cardetail_cartype_parking_isavailable"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cardetail",
            old_name="carOwnerNumber",
            new_name="ownerNumber",
        ),
        migrations.RenameField(
            model_name="cardetail",
            old_name="carNumber",
            new_name="vehicleNumber",
        ),
        migrations.RenameField(
            model_name="cardetail",
            old_name="carOwner",
            new_name="vehicleOwner",
        ),
        migrations.RenameField(
            model_name="cardetail",
            old_name="carType",
            new_name="vehicleType",
        ),
    ]
