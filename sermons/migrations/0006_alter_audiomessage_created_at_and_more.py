# Generated by Django 5.0 on 2024-10-07 15:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sermons', '0005_alter_audiomessage_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiomessage',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='videomessage',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
