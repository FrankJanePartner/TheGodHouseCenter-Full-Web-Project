# Generated by Django 5.0 on 2023-12-08 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_alter_event_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.FileField(upload_to='EventsImage'),
        ),
    ]
