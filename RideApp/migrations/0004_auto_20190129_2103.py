# Generated by Django 2.1.5 on 2019-01-30 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RideApp', '0003_auto_20190129_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(choices=[('Driver', 'Driver'), ('Sharer', 'Sharer'), ('Owner', 'Owner')], max_length=10),
        ),
    ]
