"""rideSharing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from RideApp import views as views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.register),
    path('admin/', admin.site.urls),
    path('register/', views.register, name = 'register'),
    path('login/', views.login_view, name = 'login'),
    path('role/', views.chooseRole, name = 'choose-role'),
    path('editrole/', views.editRole, name = 'edit-role'),
    path('logout/', views.logout_view, name = 'logout'),
    path('profile/', views.profile, name = 'profile'),
    path('allRides/', login_required(views.RideListView.as_view()), name = 'user-rides'),
    path('allRides/<int:ride_id>/', login_required(views.RideDetailView.as_view()), name = 'ride-detail'),
    path('ridescreate/', views.RideCreate, name = 'create-new-ride')
    # path('rides/<int:ride_id>/edit', login_required(views.RideUpdateView.as_view()), name = 'ride-edit'),
    # path('rides/search'),
    # path('rides/<int:ride_id>/join/', views.RideJoin, name = 'join-ride'),
    # path('rides/<int:pk>/confirm/')
]
