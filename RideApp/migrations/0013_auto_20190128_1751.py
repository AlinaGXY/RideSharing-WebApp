# Generated by Django 2.1.5 on 2019-01-28 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RideApp', '0012_auto_20190128_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(choices=[('Owner', 'Owner'), ('Sharer', 'Sharer'), ('Driver', 'Driver')], max_length=10),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='plate_number',
            field=models.CharField(max_length=150),
        ),
    ]
