# Generated by Django 4.2.7 on 2023-11-20 12:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_alter_category_options_alter_leader_options_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="location",
            old_name="adress",
            new_name="address",
        ),
        migrations.AlterField(
            model_name="location",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]