from django.urls import path,include
from rest_framework.routers import DefaultRouter
from api import views

router=DefaultRouter()
router.register('persons',views.PersonViewSet)
router.register('questions',views.QuestionViewSet)
router.register('answers',views.AnswerViewSet)
router.register('person-user',views.PersonOnlyViewSet)
router.register('organizers',views.OrganizerViewSet)
router.register('users',views.UserViewSet)
router.register('events',views.EventViewSet)
router.register('event',views.SingleEventViewSet)
router.register('images',views.ImageViewSet)
router.register('notifications',views.NotificationViewSet)
router.register('reviews',views.ReviewViewSet)
router.register('user-bookings',views.UserBookingViewSet)
router.register('portfolio',views.PortfolioViewSet)
router.register('event-bookings',views.EventBookingViewSet)
router.register('event_schedule',views.ScheduleViewSet)
urlpatterns=[
    path('',include(router.urls)),
    path('users/update/<id>', views.update_user,name="Update-User"),
    path('events/update/<id>', views.toggle_isFull,name="Toggle isFull"),
    path('organizers/update/<id>', views.update_user,name="Update-Organizer"),
    path('api-auth/', include('rest_framework.urls')),

]