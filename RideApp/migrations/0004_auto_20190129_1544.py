# Generated by Django 2.1.5 on 2019-01-29 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RideApp', '0003_auto_20190129_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(choices=[('Driver', 'Driver'), ('Owner', 'Owner'), ('Sharer', 'Sharer')], max_length=10),
        ),
    ]
