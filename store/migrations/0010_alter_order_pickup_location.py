# Generated by Django 5.0 on 2024-10-22 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_customer_phone_number_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pickup_location',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
