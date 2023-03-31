from django.urls import path

from . import views


app_name = 'Users'
urlpatterns = [
    path('', views.signup, name='signup'),
    
]