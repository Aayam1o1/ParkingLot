# Generated by Django 4.2.14 on 2024-08-12 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0018_comment_height_comment_width'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='image',
        ),
    ]
