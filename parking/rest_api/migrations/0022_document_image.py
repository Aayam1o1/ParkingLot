# Generated by Django 4.2.14 on 2024-08-22 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0021_alter_comment_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='document_images/'),
        ),
    ]
