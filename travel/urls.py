from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='Home'),
    path('tours/', views.tours, name='Tours'),
    path('tour-detail/', views.tourDetail, name='Tour-Details'),
    path('login', views.login, name='Login'),
    path('signUp', views.signUp, name='signup'),
    path('profile', views.profile , name='profile')
]