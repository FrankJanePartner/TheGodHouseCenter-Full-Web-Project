# Generated by Django 4.2.7 on 2023-12-05 11:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "churchMessages",
            "0008_remove_audiomessage_year_remove_videomessage_year_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="audiomessage",
            name="seriesDescription",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="videomessage",
            name="seriesDescription",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
    ]
