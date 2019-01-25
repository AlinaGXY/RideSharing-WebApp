from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(forms.Form):

    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class RideCreateForm(forms.ModelForm):
    class Meta:
        model = Rides
        fields = ['destination', 'arrival_time', 'shared_allowed', 'passenger_number', 'vehicle_type', 'special']

    def clean_arrival_time(self):
        data = self.cleaned_data['arrival_time']
        
        # Check if a date is not in the past. 
        if data < datetime.now():
            raise ValidationError('Invalid date time')

        # Remember to always return the cleaned data.
        return data

