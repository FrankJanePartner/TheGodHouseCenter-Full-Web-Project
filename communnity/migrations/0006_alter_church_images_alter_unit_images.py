# Generated by Django 5.0 on 2023-12-07 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communnity', '0005_alter_church_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='church',
            name='images',
            field=models.FileField(upload_to='media/church'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='images',
            field=models.FileField(upload_to='media/unit'),
        ),
    ]
