# Generated by Django 5.0 on 2024-07-28 10:28

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', tinymce.models.HTMLField()),
                ('publish_date', models.DateTimeField()),
                ('is_published', models.BooleanField(default=False)),
            ],
        ),
    ]
