# Generated by Django 2.1.5 on 2019-01-30 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RideApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(choices=[('Owner', 'Owner'), ('Sharer', 'Sharer'), ('Driver', 'Driver')], max_length=10),
        ),
    ]
