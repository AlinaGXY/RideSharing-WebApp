from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import Group
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Q
from .models import *

from .forms import *

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


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('choose-role')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def chooseRole(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            role_name = form.cleaned_data['name']
            curusr = request.user
            if Role.objects.filter(users=curusr).count():
                oldRolename = Role.objects.filter(users=curusr)[0].name
                oldrole, created = Role.objects.get_or_create(
                    name=oldRolename,
                )
                oldrole.users.remove(curusr)

            role, created = Role.objects.get_or_create(
                name = role_name,
            )
            role.users.add(request.user)

            return redirect('profile')  # TODO

        else:
            return render(request, 'choose_role.html', {'form': form})

    else:
        form = RoleForm()
    return render(request, 'choose_role.html', {'form': form})

@login_required
def editRole(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            role_name = form.cleaned_data['name']
            curusr = request.user
            oldRolename=Role.objects.filter(users=curusr)[0].name
            oldrole, created=Role.objects.get_or_create(
                name = oldRolename,
            )
            oldrole.users.remove(curusr)
            role, created = Role.objects.get_or_create(
                name = role_name,
            )
            role.users.add(request.user)

            return redirect('profile')  # TODO

        else:
            return render(request, 'choose_role.html', {'form': form})

    else:
        form = RoleForm()
    return render(request, 'choose_role.html', {'form': form})


@login_required
def profile(request):
    curusr = request.user

    Rolename=Role.objects.filter(users=curusr)[0].name
    if Vehicle.objects.filter(driver=curusr).count() !=0:
        currvehicle=Vehicle.objects.filter(driver=curusr)[0]
    else:
        currvehicle= None
    return render(request, 'profile.html',{'Rolename':Rolename,'Vehicle':currvehicle})


class RideListView(ListView):
    model = Rides
    template_name = 'rides_list.html'
    ordering = ['-arrival_time']
    context_object_name = "rides"

    def get_queryset(self):
        user = self.request.user
        rides = Rides.objects.filter(Q(passengers = user) | Q(driver = user.username))
        return rides

class RideDetailView(DetailView):
    model = Rides
    template_name = 'rides_detail.html'
    context_object_name = "ride"


# https://docs.djangoproject.com/zh-hans/2.1/ref/contrib/messages/#displaying-messages
@login_required
def RideCreate(request):
    if Role.objects.filter(users = request.user)[0].name != "Owner":
        messages.add_message(request, messages.INFO, 'Oops! You can only request a new ride as an owner.')
        return redirect('profile')

    if request.method == 'POST':
        form = RideCreateForm(request.POST)
        if form.is_valid():
            ride = form.save()
            if ride.shared_allowed:
                s, created = RideStatus.objects.get_or_create(name = "public")
                ride.status = s
            else:
                s, created = RideStatus.objects.get_or_create(name = "private")
                ride.status = s
            ride.owner = request.user.username
            ride.passengers.add(request.user)
            ride.save()
            return redirect('profile')
        else:
            messages.add_message(request, messages.INFO, "Invalid input!")
            return render(request, 'create_ride.html', {'form': form})
    else:
        form = RideCreateForm()

    return render(request, 'create_ride.html', {'form': form})


def addVehicle(request):
    if Role.objects.filter(users = request.user)[0].name != "Driver":
        messages.add_message(request, messages.INFO, 'Oops! You can only add a vehicle as an driver.')
        return redirect('profile')

    if Vehicle.objects.filter(driver = request.user).count() == 1:
        messages.add_message(request, messages.INFO, 'Oops! You have already register your car. Maybe you want to edit your car?')
        return redirect('profile')

    if request.method == 'POST':
        form = VehicleCreateForm(request.POST)
        if form.is_valid():
            car = form.save()
            car.driver = request.user
            car.save()
            return redirect('profile')
        else:
            return render(request, 'create_vehicle.html', {'form': form})
    else:
        messages.add_message(request, messages.INFO, "Invalid input!")
        form = VehicleCreateForm()

    return render(request, 'create_vehicle.html', {'form': form})


class RideUpdateView(UpdateView):
    model = Rides
    #fields = ['destination', 'arrival_time', 'shared_allowed', 'passenger_number', 'vehicle_type', 'special']
    template_name = 'ride_edit.html'
    context_object_name = 'ride'
    form_class = RideCreateForm

    def form_valid(self, form):
        ride = form.save()
        self.object = ride
        if ride.shared_allowed:
            s, created = RideStatus.objects.get_or_create(name = "public")
            self.object.status = s
        else:
            s, created = RideStatus.objects.get_or_create(name = "private")
            self.object.status = s
        
        return redirect("user-rides")

        


# def SharerRequestCreate(request):


# @login_required
# def SharerSearch(request, user_id):
#     user = request.user
#     if Role.objects.filter(users = user)[0].name != "Sharer":
#         return redirect('profile')




# @login_required
# def RideJoin(request, ride_id):
#     # TODO: check status and decide if join is valid
#     user = request.user
#     user.groups.add("Sharer")
#     ride = Rides.objects.get(pk = ride_id)
#     ride.status = 'shared'
#     ride.passengers.add(user)
#     ride.save()
#     return render(request, 'rides_list.html')