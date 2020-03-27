from django.urls import path,include
from rest_framework.routers import DefaultRouter
from api import views

router=DefaultRouter()
router.register('persons',views.PersonViewSet)
router.register('person-user',views.PersonOnlyViewSet)
router.register('organizers',views.OrganizerViewSet)
router.register('users',views.UserViewSet)
router.register('events',views.EventViewSet)
router.register('images',views.ImageViewSet)
router.register('event_schedule',views.ScheduleViewSet)
urlpatterns=[
    path('',include(router.urls)),
    path('users/update/<id>', views.update_user,name="Update-User"),
    path('api-auth/', include('rest_framework.urls')),

]