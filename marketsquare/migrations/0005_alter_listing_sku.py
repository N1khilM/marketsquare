# Generated by Django 5.0.6 on 2024-06-30 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketsquare', '0004_listing_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='sku',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
