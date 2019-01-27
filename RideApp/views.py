from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import Group
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

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
    return render(request, 'profile.html',{'Rolename':Rolename})

class RideListView(ListView):
    model = Rides
    template_name = 'rides_list.html'
    ordering = ['-arrival_time']
    context_object_name = "rides"

    def get_queryset(self):
        user = self.request.user
        rides = Ride.objects.filter(passenger = user, driver = user.username)
        return rides

class RideDetailView(DetailView):
    model = Rides
    template_name = 'rides_detail.html'
    context_object_name = "context"

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(RideDetailView, self).get_context_data(**kwargs)
    #     context['ride'] = self.request['ride_id']
    #     return context

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
            ride.save()
            return redirect('profile')
        else:
            return render(request, 'create_ride.html', {'form': form})
    else:
        form = RideCreateForm()

    return render(request, 'create_ride.html', {'form': form})

# @method_decorator(login_required, name='dispatch')
# class RideUpdateView(UpdateView):
#     model = Ride
#     fields = ['destination', 'arrival_time', 'shared_allowed', 'passenger_number', 'vehicle_type', 'special']
#     template_name = 'ride_edit.html'
#     context_object_name = 'ride'


# @login_required
# def RideSearch(request, user_id):
#     user = request.user
#     if user.groups.filter(name = 'Driver').exists():
#         result = Rides.objects.filter(status=)


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