# Generated by Django 5.0 on 2024-03-21 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WholeWordConference', '0004_remove_attendee_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendee',
            name='local_church',
        ),
        migrations.AlterField(
            model_name='attendee',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='godhouse_location',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='how_did_you_know',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='how_will_you_attend',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='ministry',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='ministry_status',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='need_accommodation',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='phone',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
