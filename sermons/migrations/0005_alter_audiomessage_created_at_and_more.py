# Generated by Django 5.0 on 2024-10-07 15:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sermons', '0004_alter_audiomessage_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiomessage',
            name='created_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='videomessage',
            name='created_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]