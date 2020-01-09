from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='Home'),
    path('tours/', views.tours, name='Tours'),
    path('tour/detail/', views.tourDetail, name='Tour-Details'),
    path('login/', views.login, name='Login'),
    path('register/', views.signUp, name='Signup'),
    path('dashboard/', views.dashboard , name='dashboard'),
    path('dashboard/eventBooking/', views.eventBooking , name='Event-Booking'),
    path('dashboard/myProfile/', views.myProfile , name='My-Profile'),
    path('dashboard/myProfile/edit/', views.editProfile , name='Edit-Profile'),
    path('contact/',views.contact, name='Contact'),
    path('404/',views.not_found, name='404'),
    path('about/',views.about, name='About'),
    path('price-list/',views.price_list, name='Price-Lists'),
]