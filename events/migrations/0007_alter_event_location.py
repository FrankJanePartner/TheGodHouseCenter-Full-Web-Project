# Generated by Django 5.0 on 2023-12-19 14:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_remove_leadersocialmedia_leader_and_more'),
        ('events', '0006_event_button_text_alter_event_register_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.location'),
        ),
    ]
