"""FitTracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from knox import views as knox_views

from .views import FoodLogView, quotes, hm, Dashboard
from .views import FoodLogView, quotes, ExerciseLogView, MeasurementsLogView
from .views_account import AccountView, LoginAPI, ProfileView, ChangePassword, logoutUser
from .views_scanner import Scanner

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('fitness/', include('Fitness.urls')),
    # # path('signup/', include('Users.urls')),
    # path('api-auth/', include('rest_framework.urls'))
    path("scan/<str:id>", Scanner.as_view()),
    path('account/', AccountView.as_view()),
    path('account/<int:id>/', AccountView.as_view()),
    path('profile', ProfileView.as_view()),
    path('profile/<int:id>/', ProfileView.as_view()),
    path('login/', LoginAPI.as_view(), name='login'),
    path('food-log/',FoodLogView.as_view(),name='FoodLog'),
    path('quotes/',quotes,name='quotes'),
    path('changepassword/', ChangePassword.as_view()),

    # fontend
    path('fr/register/', AccountView.as_view(fr=1), name='register'),
    path('fr/login/', LoginAPI.as_view(fr=1), name='login'),
    path('fr/profile/', ProfileView.as_view(fr=1), name='settings'),
    path('', Dashboard.as_view(fr=1), name='dashboard'),
    path('fr/logout/', logoutUser, name="logout"),


    path('e-log/',ExerciseLogView.as_view(), name = 'ExerciseLog'),
    path('index-log', MeasurementsLogView.as_view(), name = 'IndexLog')

    
]
