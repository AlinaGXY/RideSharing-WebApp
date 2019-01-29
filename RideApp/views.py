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

            return redirect('profile')  

        else:
            curusr = request.user
            Rolename = Role.objects.filter(users=curusr)[0].name
            return render(request, 'choose_role.html', {'form': form, 'Rolename':Rolename})

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
            curusr = request.user
            Rolename = Role.objects.filter(users=curusr)[0].name
            return render(request, 'choose_role.html', {'form': form, "Rolename":Rolename})

    else:
        form = RoleForm()
    curusr = request.user
    Rolename = Role.objects.filter(users=curusr)[0].name
    return render(request, 'choose_role.html', {'form': form, "Rolename":Rolename})


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
        if Role.objects.filter(users = user)[0].name == 'Driver':
            rides = Rides.objects.filter(Q(driver = user.username))
        else:
            rides = Rides.objects.filter(Q(passengers = user))
        return rides

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        curusr = self.request.user
        context['Rolename'] = Role.objects.filter(users=curusr)[0].name
        return context



class RideDetailView(DetailView):
    model = Rides
    template_name = 'rides_detail.html'
    context_object_name = "ride"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        curusr = self.request.user
        context['Rolename'] = Role.objects.filter(users=curusr)[0].name
        return context


# https://docs.djangoproject.com/zh-hans/2.1/ref/contrib/messages/#displaying-messages
@login_required
def RideCreate(request):
    curusr = request.user
    Rolename = Role.objects.filter(users=curusr)[0].name
    if Rolename != "Owner":
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
            return render(request, 'create_ride.html', {'form': form, "Rolename":Rolename})
    else:
        form = RideCreateForm()

    return render(request, 'create_ride.html', {'form': form, "Rolename":Rolename})


def addVehicle(request):
    curusr = request.user
    Rolename = Role.objects.filter(users=curusr)[0].name
    if Rolename != "Driver":
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
            return render(request, 'create_vehicle.html', {'form': form, "Rolename":Rolename})
    else:
        messages.add_message(request, messages.INFO, "Invalid input!")
        form = VehicleCreateForm()

    return render(request, 'create_vehicle.html', {'form': form, "Rolename": Rolename})


class RideUpdateView(UpdateView):
    model = Rides
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
        self.object.save()
        return redirect("user-rides")


@login_required
def DriverSearch(request):
    user = request.user
    Rolename = Role.objects.filter(users=user)[0].name
    if Rolename != "Driver":
        return redirect('profile')

    vehicle = Vehicle.objects.filter(driver=user)[0]
    # open type special capacity
    result = Rides.objects.filter(
        status__name__in=['public', 'private'], 
        passenger_number__lt=vehicle.capacity,
        vehicle_type__in=['', vehicle.type],
        special__in=['', vehicle.special]
    )
    return render(request, 'driver_search.html', {'rides':result, "Rolename":Rolename})


def SharerSearch(request):
    user = request.user
    Rolename = Role.objects.filter(users=user)[0].name
    if Rolename != "Sharer":
        return redirect('profile')

    condition = SharerRequest.objects.filter(sharer = user)
    if (condition.count() == 0):
        return redirect('sharer-request-create')

    condition = condition[0]
    result = Rides.objects.filter(
        status__name='public',
        destination=condition.destination,
        passenger_number__lt=condition.passenger_number,
        arrival_time__gte=condition.earliest_time,
        arrival_time__lte=condition.latest_time
    )
    return render(request, 'sharer_search.html', 
                {'rides':result, "Rolename":Rolename, "condition":condition})


def RideConfirm(request, ride_id):
    user = request.user
    ride = Rides.objects.get(pk=ride_id)
    if ride.status.name != "confirmed" and ride.status.name != "completed":
        s, created = RideStatus.objects.get_or_create(name = "confirmed")
        ride.status = s
        ride.driver = user.username
        ride.save()
        return redirect('user-rides')
    else:
        messages.add_message(request, messages.INFO, "This ride has been confirmed by others!")
        return redirect('driver-search')


def RideComplete(request, ride_id):
    user = request.user
    ride = Rides.objects.get(pk=ride_id)
    if ride.status.name == "confirmed" and ride.driver == user.username:
        s, created = RideStatus.objects.get_or_create(name = "completed")
        ride.status = s
        ride.save()
        return redirect('user-rides')
    else:
        messages.add_message(request, messages.INFO, "Ride can only be completed by the driver!")
        return redirect('user-rides')


def SharerRequestCreate(request):
    user = request.user

    Rolename = Role.objects.filter(users=user)[0].name
    if Rolename != "Sharer":
        messages.add_message(request, messages.INFO, 'Oops! You can only add a vehicle as an sharer.')
        return redirect('profile')
    if request.method == 'POST':
        form = SharerRequestCreateForm(request.POST)
        if form.is_valid():
            condition = form.save()
            condition.sharer = user
            currReq = SharerRequest.objects.filter(sharer=user)
            if currReq.count() == 0:
                condition.save()
            else:
                currReq[0] = condition
                currReq[0].save()
            return redirect('profile') # TODO
        else:
            return render(request, 'sharer_condition.html', {'form': form,"Rolename":Rolename})
    else:
        form = SharerRequestCreateForm()

    return render(request, 'sharer_condition.html', {'form': form, "Rolename":Rolename})


class SharerRequestUpdateView(UpdateView):
    model = Rides
    template_name = 'sharer_condition.html'
    context_object_name = 'condition'
    form_class = SharerRequestCreateForm


def RideJoin(request, ride_id):
    user = request.user
    ride = Rides.objects.get(pk = ride_id)
    if ride.status.name == "public":
        s, created = RideStatus.objects.get_or_create(name = "shared")
        ride.status = s
        ride.passengers.add(user)
        ride.passenger_number += SharerRequest.objects.filter(sharer=user)[0].passenger_number
        ride.save()
        return redirect('user-rides')
    else:
        messages.add_message(request, messages.INFO, 'Currently you can not join this ride')
        return redirect('sharer-search')