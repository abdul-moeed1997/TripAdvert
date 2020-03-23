from django.conf.urls import url
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='Home'),
    url(r'^accounts/',include('allauth.urls')),
    path('tours/', views.tours, name='Tours'),
    path('ajax/', views.ajax),
    path('organizer/addEvent/', views.addEvent, name='Add-Event'),
    path('tour/detail/<id>', views.tourDetail, name='Tour-Details'),
    path('organizer/detail/', views.organizerDetail, name='Organizer-Detail'),
    path('organizer/detail/portfolio/', views.organizerPortfolioUser, name='Organizer-Detail'),
    path('login/', views.login, name='Login'),
    path('logout/', views.logout, name='Logout'),
    path('user/register/', views.signUp, name='Signup'),
    path('specialEvent/', views.specialEvent , name='specialEvent'),
    path('tips/', views.tips , name='tips'),
    path('faq/', views.faq , name='faq'),
    path('user/dashboard/eventBooking/', views.eventBooking , name='Event-Booking'),
    path('user/dashboard/myProfile/', views.myProfile , name='My-Profile'),
    path('organizer/dashboard/myProfile/', views.organizerProfile , name='dashboard'),
    path('organizer/dashboard/myProfile/portfolio/', views.organizerPortfolio , name='dashboard'),
    path('organizer/dashboard/myProfile/events/', views.organizerEvents , name='OrganizerEvents'),
    path('user/dashboard/myProfile/edit/', views.editProfile , name='Edit-Profile'),
    path('organizer/dashboard/myProfile/edit/', views.editProfileOrganizer , name='Edit-Profile'),
    path('contact/',views.contact, name='Contact'),
    path('404/',views.not_found, name='404'),
    path('about/',views.about, name='About'),
    path('price-list/',views.price_list, name='Price-Lists'),
    path('booking-receipt/',views.eventBookingDetails,name='booking-Details'),
    path('organizer/register/',views.organizerSignUp, name='org-signUp'),
    path('forgot-pass/', views.forgotPassword,name='forgot-password'),
    path('email-forgot-pass/', views.EmailforgotPassword,name='forgot-password')
]