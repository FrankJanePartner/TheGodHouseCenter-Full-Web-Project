# Generated by Django 5.0 on 2024-08-12 15:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shekinah', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lifeperformance',
            options={'verbose_name_plural': 'LifePerformances'},
        ),
        migrations.RemoveField(
            model_name='lifeperformance',
            name='images',
        ),
        migrations.RemoveField(
            model_name='lifeperformance',
            name='uploaded_at',
        ),
        migrations.CreateModel(
            name='LifePerformanceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(default='images/default.png', help_text='Upload a LifePerformance image', upload_to='products/', verbose_name='image')),
                ('alt_text', models.CharField(blank=True, help_text='Please add alturnative text', max_length=255, null=True, verbose_name='Alturnative text')),
                ('is_feature', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lifePerformance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_image', to='shekinah.lifeperformance')),
            ],
            options={
                'verbose_name': 'LifePerformanceImage',
                'verbose_name_plural': 'LifePerformanceImages',
            },
        ),
    ]