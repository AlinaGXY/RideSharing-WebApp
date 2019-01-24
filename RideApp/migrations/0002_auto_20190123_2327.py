# Generated by Django 2.1.5 on 2019-01-24 04:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RideApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='id',
            field=models.AutoField(auto_created=True, default='car', primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='driver',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
