# Generated by Django 4.2.7 on 2023-11-27 13:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_rename_adress_location_address_alter_location_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="category",
            old_name="status",
            new_name="description",
        ),
    ]
