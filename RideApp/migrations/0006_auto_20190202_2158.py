# Generated by Django 2.1.5 on 2019-02-03 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RideApp', '0005_auto_20190202_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(choices=[('Sharer', 'Sharer'), ('Driver', 'Driver'), ('Owner', 'Owner')], max_length=10),
        ),
    ]
