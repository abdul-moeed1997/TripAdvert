import django_filters
from django.contrib import auth
from django.contrib.auth.hashers import make_password
import django.contrib.auth.hashers as hasher
from django.db.transaction import atomic
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view

from django.db.models import Avg, Max, Min, Sum, Count
from api import serializers, models

from django.http import JsonResponse
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from requests.exceptions import HTTPError

from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
from . import serializers



class UserBookingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BookingSerializer
    queryset = models.Booking.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['user']


class PortfolioViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PortfolioSerializer
    queryset = models.Event.objects.filter()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['organizer','is_completed']

class EventBookingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BookingSerializer
    queryset = models.Booking.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['event']

class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventScheduleSerializer
    queryset = models.EventSchedule.objects.all()

class PersonOnlyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PersonOnlySerializer
    queryset = models.Person.objects.all()

class OrganizerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrganizerSerializer
    queryset = models.Organizer.objects.all()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ImageSerializer
    queryset = models.Image.objects.all()


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.filter(is_completed=False,is_full=False).order_by('-date')


class SingleEventViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SingleEventSerializer
    queryset = models.Event.objects.all()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

class OrganizerView(viewsets.ModelViewSet):
    serializer_class = serializers.OrganizerSerializer
    queryset = models.Organizer.objects.all()

class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PersonSerializer
    queryset = models.Person.objects.filter(is_blocked=False)
    search_fields = ('first_name','last_name', 'email',)

    @action(detail=False, methods=['post'])
    def login(self, request):
        data=request.data
        user = self.queryset.filter(email=request.data['email'])
        if user:
            if hasher.check_password(request.data['password'],user.first().get_password()):
                serializer = serializers.PersonSerializer(user,many=True)
                return Response(status=status.HTTP_200_OK, data=serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST,data="Invalid Email or Password")


@api_view(['PUT',])
def toggle_isFull(request,id):
    event = models.Event.objects.get(id=id)
    if event:
        if event.is_full:
            event.is_full=False
        else:
            event.is_full=True
        event.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT',])
@atomic
def update_user(request,id):
    if request.data["user_type"]=="1":
        user = models.User.objects.get(id=request.data["user"])
        serializer = serializers.UserSerializer(user,data={"address":request.data["address"]})
        if serializer.is_valid():
            serializer.save()

    elif request.data["user_type"]=="2":
        organizer = models.Organizer.objects.get(id=request.data["organizer"])
        serializer = serializers.OrganizerSerializer(organizer,data={"address":request.data["address"],"experience":request.data["experience"],"organization":request.data["organization"]})
        if serializer.is_valid():
            serializer.save()

        data = str(serializer.errors)
    person = models.Person.objects.get(id=id)
    data = {"first_name":request.data["first_name"],"last_name":request.data["last_name"],"phone_no":request.data["phone_no"]}
    if "image" in request.data:
        data["image"]=request.data["image"]
    else:
        data["image"] = person.image
    serializer = serializers.PersonOnlySerializer(person,data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    data += str(serializer.errors)
    return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
