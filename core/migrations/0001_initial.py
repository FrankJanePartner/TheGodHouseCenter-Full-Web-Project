# Generated by Django 4.2.6 on 2023-11-13 16:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('class_id', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Church',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('class_id', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('images', models.ImageField(upload_to='media/churches')),
            ],
            options={
                'verbose_name': 'Churches',
            },
        ),
        migrations.CreateModel(
            name='Leader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('class_id', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('images', models.ImageField(upload_to='media/leader')),
                ('position', models.TextField()),
                ('bio', models.TextField()),
            ],
            options={
                'verbose_name': 'Leaders',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_id', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=255)),
                ('adress', models.TextField()),
            ],
            options={
                'verbose_name': 'Locations',
            },
        ),
    ]
