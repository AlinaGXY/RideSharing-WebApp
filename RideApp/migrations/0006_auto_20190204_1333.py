# Generated by Django 2.1.5 on 2019-02-04 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RideApp', '0005_auto_20190204_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(choices=[('Sharer', 'Sharer'), ('Owner', 'Owner'), ('Driver', 'Driver')], max_length=10),
        ),
    ]
