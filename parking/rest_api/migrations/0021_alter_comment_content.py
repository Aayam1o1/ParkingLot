# Generated by Django 4.2.14 on 2024-08-12 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0020_comment_comment_alter_comment_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(),
        ),
    ]
