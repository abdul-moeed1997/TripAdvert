from django.urls import path,include
from rest_framework.routers import DefaultRouter
from api import views

router=DefaultRouter()
router.register('persons',views.PersonViewSet)
router.register('events',views.EventViewSet)
router.register('images',views.ImageViewSet)
urlpatterns=[
    path('',include(router.urls)),

]