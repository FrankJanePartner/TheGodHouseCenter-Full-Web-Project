# Generated by Django 5.0 on 2024-04-03 09:19

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sermons', '0002_alter_videomessage_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiomessage',
            name='seriesDescription',
            field=tinymce.models.HTMLField(),
        ),
    ]
