from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Rides(models.Model):
    passengers = models.ManyToManyField(User)
    owner = models.EmailField(max_length=254)
    destination = models.CharField(max_length = 100)
    passenger_number = models.IntegerField(blank = False)
    arrival_time = models.DateTimeField(default = timezone.now)
    shared_allowed = models.BooleanField(default = True)
    vehicle_type = models.CharField(max_length = 100)
    special = models.TextField()
    status = models.CharField(max_length = 100)
    driver = models.CharField(max_length = 100)

    def __str__(self):
        return self.owner

class Vehicle(models.Model):
    driver = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null = True
    )
    type = models.CharField(max_length=150,blank=False)
    capacity = models.IntegerField(blank=False)
    special = models.TextField()

    def __str__(self):
        return self.driver