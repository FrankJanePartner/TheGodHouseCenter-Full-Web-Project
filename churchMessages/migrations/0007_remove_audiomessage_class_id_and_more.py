# Generated by Django 4.2.7 on 2023-12-01 12:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("churchMessages", "0006_rename_video_id_audiomessage_audio_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="audiomessage",
            name="class_id",
        ),
        migrations.RemoveField(
            model_name="videomessage",
            name="class_id",
        ),
    ]
