# Generated by Django 4.2.6 on 2023-11-14 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communnity', '0002_church'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='church',
            options={'verbose_name_plural': 'Churches'},
        ),
        migrations.AlterModelOptions(
            name='unit',
            options={'verbose_name_plural': 'Units'},
        ),
    ]
