# Generated by Django 5.0.6 on 2024-07-11 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0020_ownerprofile"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cardetail",
            old_name="owner_name",
            new_name="owner",
        ),
    ]
