from django.urls import path,include
from rest_framework.routers import DefaultRouter
from api import views

router=DefaultRouter()
router.register('person-user',views.PersonOnlyViewSet,basename="person user")
router.register('persons',views.PersonViewSet,basename=" persons")
router.register('questions',views.QuestionViewSet)
router.register('answers',views.AnswerViewSet)
router.register('organizers',views.OrganizerViewSet)
router.register('users',views.UserViewSet)
router.register('events',views.EventViewSet)
router.register('general-events',views.GeneralEventViewSet)
router.register('event',views.SingleEventViewSet)
router.register('images',views.ImageViewSet)
router.register('notifications',views.NotificationViewSet)
router.register('reviews',views.ReviewViewSet)
router.register('user-bookings',views.UserBookingViewSet)
router.register('portfolio',views.PortfolioViewSet)
router.register('event-bookings',views.EventBookingViewSet)
router.register('event-schedule',views.ScheduleViewSet)
urlpatterns=[
    path('',include(router.urls)),
    path('users/update/<id>', views.update_user,name="Update-User"),
    path('events/update/<id>', views.toggle_isFull,name="Toggle isFull"),
    path('bookings/update/<id>', views.toggle_isVerified, name="Toggle isVerified"),
    path('organizers/update/<id>', views.update_user,name="Update-Organizer"),
    path('events/reviewed/<id>',views.reviewed_user_events,name="reviewed events"),
    path('events/pending/<id>',views.pending_user_events,name="pending events"),
    path('persons/set_firebase_token/<id>',views.setFirebaseInstanceToken,name="set firebase token"),
    path('api-auth/', include('rest_framework.urls')),

]