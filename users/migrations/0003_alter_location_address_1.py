# Generated by Django 5.0.6 on 2024-06-30 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_location_state_alter_location_zip_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='address_1',
            field=models.CharField(max_length=128),
        ),
    ]
