# Generated by Django 5.0 on 2023-12-09 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communnity', '0009_alter_church_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='church',
            name='images',
        ),
    ]
