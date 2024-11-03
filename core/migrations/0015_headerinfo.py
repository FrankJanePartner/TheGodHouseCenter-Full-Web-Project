# Generated by Django 5.0 on 2023-12-08 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_serviceday_center'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeaderInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_text', models.CharField(max_length=255)),
                ('link', models.URLField()),
            ],
            options={
                'verbose_name_plural': 'HeaderInfos',
            },
        ),
    ]
