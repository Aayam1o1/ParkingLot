# Generated by Django 4.2.14 on 2024-08-07 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0016_comment_whole_page_alter_comment_x1_alter_comment_x2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
