from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class RideStatus(models.Model):
    # rides = models.ManyToManyField(Rides, null=True)
    name = models.CharField(max_length = 10)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Rides(models.Model):
    passengers = models.ManyToManyField(User)
    owner = models.CharField(max_length=100)
    destination = models.CharField(max_length = 100)
    passenger_number = models.IntegerField(blank = False)
    arrival_time = models.DateTimeField(default = timezone.now)
    shared_allowed = models.BooleanField(default = True)
    vehicle_type = models.CharField(max_length = 100)
    special = models.TextField(blank=True)
    status = models.ForeignKey(RideStatus, on_delete=models.CASCADE)
    driver = models.CharField(max_length = 100)

    def __str__(self):
        return self.owner

class Role(models.Model):
    Role_Choices = {
    ('Owner', 'Owner'),
    ('Sharer', 'Sharer'),
    ('Driver', 'Driver'),
    }
    users = models.ManyToManyField(User)
    name = models.CharField(max_length = 10, choices = Role_Choices)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Vehicle(models.Model):
    driver = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null = True
    )
    type = models.CharField(max_length=150)
    capacity = models.IntegerField(blank=False)
    special = models.TextField()

    def __str__(self):
        return self.driver

    class Meta:
        ordering = ('driver',)

