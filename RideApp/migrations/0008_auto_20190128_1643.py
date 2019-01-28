# Generated by Django 2.1.5 on 2019-01-28 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RideApp', '0007_auto_20190128_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rides',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='RideApp.RideStatus'),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(choices=[('Driver', 'Driver'), ('Owner', 'Owner'), ('Sharer', 'Sharer')], max_length=10),
        ),
    ]
