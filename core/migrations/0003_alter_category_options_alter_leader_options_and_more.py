# Generated by Django 4.2.6 on 2023-11-14 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_delete_church'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='leader',
            options={'verbose_name_plural': 'Leaders'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name_plural': 'Locations'},
        ),
    ]
