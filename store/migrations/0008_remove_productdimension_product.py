# Generated by Django 5.0 on 2024-10-20 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_productdimension_productdimensionvalue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productdimension',
            name='product',
        ),
    ]
