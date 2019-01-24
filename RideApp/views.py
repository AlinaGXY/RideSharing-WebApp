from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import Group
from django.views.generic import ListView, DetailView

from .models import Rides, Vehicle

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form' : form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect('profile')

        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
class RideListView(ListView):
    model = Rides
    template_name = 'rides_list.html'
    ordering = ['-arrival_time']
    context_object_name

    def get_queryset(self):
        if user.group.filter(name = 'Driver'):
            rides = Rides.objects.filter(driver = user.username)
        else:
            rides = User.objects.filter(passenger = user)
        return rides

class RideDetailView(DetailView):
    model = Rides
    template_name = 'rides_detail.html'