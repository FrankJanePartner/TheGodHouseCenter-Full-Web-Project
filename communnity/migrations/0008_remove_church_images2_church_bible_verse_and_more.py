# Generated by Django 5.0 on 2023-12-09 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communnity', '0007_church_images2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='church',
            name='images2',
        ),
        migrations.AddField(
            model_name='church',
            name='Bible_verse',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='church',
            name='description2',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='church',
            name='quote',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='church',
            name='slogan',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]