# Generated by Django 4.1 on 2022-08-10 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrap_pickups_app', '0002_profile_pickup'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSavedLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrap_pickups_app.profile')),
            ],
        ),
    ]