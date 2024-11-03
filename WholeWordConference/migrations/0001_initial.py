# Generated by Django 5.0 on 2024-03-08 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('ministry', models.CharField(max_length=255)),
                ('ministry_status', models.CharField(choices=[('member', 'Member'), ('worker', 'Worker'), ('minister/leader', 'Minister/Leader'), ('pastor', 'Pastor')], max_length=50)),
                ('how_did_you_know', models.CharField(choices=[('godhouse', 'Godhouse'), ('social media', 'Social media'), ('friend', 'Friend'), ('banner/poster', 'Banner/Poster'), ('others', 'others')], max_length=50)),
                ('how_will_you_attend', models.CharField(choices=[('physical attendance', 'Physical attendance'), ('online attendance', 'Online attendance')], max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('location', models.CharField(max_length=255)),
                ('local_church', models.CharField(max_length=255)),
                ('godhouse_location', models.CharField(max_length=50)),
                ('need_accommodation', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3)),
            ],
            options={
                'verbose_name_plural': 'Registrations',
            },
        ),
    ]