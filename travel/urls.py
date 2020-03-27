from django.conf.urls import url
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='Home'),
    url(r'^accounts/',include('allauth.urls')),
    path('tours/', views.tours, name='Tours'),
    path('user-profile/', views.user_profile, name='User-Profile'),
    path('access-denied/', views.access_denied, name='Access-Denied'),
    path('something-wrong/', views.something_wrong, name='Something-Wrong'),
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
    path('user/dashboard/event-booking/', views.eventBooking , name='Event-Booking'),
    path('user/dashboard/my-profile/', views.userMyProfile , name='My-Profile'),
    path('organizer/dashboard/my-profile/', views.organizerProfile , name='dashboard'),
    path('organizer/dashboard/my-profile/portfolio/', views.organizerPortfolio , name='dashboard'),
    path('organizer/dashboard/my-profile/events/', views.organizerEvents , name='OrganizerEvents'),
    path('user/dashboard/my-profile/edit/', views.userEditProfile , name='Edit-Profile'),
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