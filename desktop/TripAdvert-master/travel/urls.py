from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='Home'),
    path('login', views.login, name='Login'),
    path('signUp', views.signUp, name='signup'),
    path('profile', views.profile , name='profile')
]