# Generated by Django 4.1 on 2022-08-12 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap_pickups_app', '0006_alter_pickup_scrap_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pickup',
            name='phone',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
