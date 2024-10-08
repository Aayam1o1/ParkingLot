# Generated by Django 4.2.14 on 2024-08-06 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0014_document_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='end_offset',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='start_offset',
        ),
        migrations.AddField(
            model_name='comment',
            name='x1',
            field=models.FloatField(default=23),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='x2',
            field=models.FloatField(default=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='y1',
            field=models.FloatField(default=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='y2',
            field=models.FloatField(default=5),
            preserve_default=False,
        ),
    ]
