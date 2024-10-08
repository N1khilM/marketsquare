# Generated by Django 5.0.6 on 2024-06-29 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketsquare', '0002_rename_engine_listing_product_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='dimensions',
            new_name='size',
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=10),
        ),
        migrations.AlterField(
            model_name='listing',
            name='sku',
            field=models.CharField(default='1', max_length=64),
        ),
    ]
