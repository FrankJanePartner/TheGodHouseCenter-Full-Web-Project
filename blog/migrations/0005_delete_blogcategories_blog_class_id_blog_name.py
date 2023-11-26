# Generated by Django 4.2.7 on 2023-11-26 07:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_delete_subscriber"),
    ]

    operations = [
        migrations.DeleteModel(
            name="BlogCategories",
        ),
        migrations.AddField(
            model_name="blog",
            name="class_id",
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="blog",
            name="name",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
    ]