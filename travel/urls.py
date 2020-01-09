from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='Home'),
    path('tours/', views.tours, name='Tours'),
    path('tour/detail/', views.tourDetail, name='Tour-Details'),
    path('login/', views.login, name='Login'),
    path('user/register/', views.signUp, name='Signup'),
    path('user/dashboard/', views.dashboard , name='dashboard'),
    path('specialEvent/', views.specialEvent , name='specialEvent'),
    path('tips/', views.tips , name='tips'),
    path('faq/', views.faq , name='faq'),
    path('user/dashboard/eventBooking/', views.eventBooking , name='Event-Booking'),
    path('user/dashboard/myProfile/', views.myProfile , name='My-Profile'),
    path('user/dashboard/myProfile/edit/', views.editProfile , name='Edit-Profile'),
    path('contact/',views.contact, name='Contact'),
    path('404/',views.not_found, name='404'),
    path('about/',views.about, name='About'),
    path('price-list/',views.price_list, name='Price-Lists'),
    path('booking-receipt/',views.eventBookingDetails,name='booking-Details'),
    path('organizer/signUp/',views.organizerSignUp, name='org-signUp'),
    path('forgot-pass/', views.forgotPassword,name='forgot-password'),
    path('email-forgot-pass/', views.EmailforgotPassword,name='forgot-password')
]