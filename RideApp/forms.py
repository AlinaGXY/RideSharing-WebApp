from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import *
from django.core.exceptions import ValidationError
class UserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(forms.Form):

    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class RoleForm(forms.Form):
    Role_Choices = {
        ('Owner', 'Owner'),
        ('Sharer', 'Sharer'),
        ('Driver', 'Driver'),
    }
    name=forms.ChoiceField(choices=Role_Choices)
    class Meta:
        model = Role
        fields = ("name")

class RideCreateForm(forms.ModelForm):
    destination = models.CharField(max_length = 100)
    passenger_number = models.IntegerField(blank = False)
    arrival_time = models.DateTimeField(default = timezone.now)
    shared_allowed = models.BooleanField(default = True)
    vehicle_type = models.CharField(max_length = 100)
    special = models.TextField()

    class Meta:
        model = Rides
        fields = ['destination', 'arrival_time', 'shared_allowed', 'passenger_number', 'vehicle_type', 'special']

    def clean_arrival_time(self):
        data = self.cleaned_data['arrival_time']
        
        # Check if a date is not in the past. 
        if data < timezone.now():
            raise ValidationError('Invalid date time')

        # Remember to always return the cleaned data.
        return data

