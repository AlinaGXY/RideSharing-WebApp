# Generated by Django 2.1.5 on 2019-02-03 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RideApp', '0002_auto_20190202_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(choices=[('Driver', 'Driver'), ('Owner', 'Owner'), ('Sharer', 'Sharer')], max_length=10),
        ),
    ]
