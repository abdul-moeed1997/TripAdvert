import os

import django_filters
from django.contrib import auth
from django.contrib.auth.hashers import make_password
import django.contrib.auth.hashers as hasher
from django.db.transaction import atomic
from django.shortcuts import render

# Create your views here.
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view

from django.db.models import Avg, Max, Min, Sum, Count

from TripAdvert import settings
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
    queryset = models.Event.objects.all()
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
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {"email":['exact']}

class OrganizerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrganizerSerializer
    queryset = models.Organizer.objects.all()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ImageSerializer
    queryset = models.Image.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['event']

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NotificationSerializer
    queryset = models.Notification.objects.all().order_by("-date")
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['sentFor']

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    queryset = models.Review.objects.all().order_by("-date")
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['organizer','user']

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.filter(is_completed=False,is_full=False).order_by('-date')
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {"home":['exact'],"destination":['exact'],"category":['exact'],"date_of_departure":['exact'],"date_of_arrival":['exact'],"price":["lte","gte"]}
    pagination_class = LargeResultsSetPagination


class SingleEventViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SingleEventSerializer
    queryset = models.Event.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    @action(detail=False, methods=['post'])
    @atomic
    def compare_events(self, request):
        ids=request.data["id"]
        ids = ids.split(",")
        data=[]
        for id in ids:
            item = self.queryset.get(id=id)
            serializer=serializers.EventSerializer(item,many=False)
            data.append(serializer.data)
        return Response(status=status.HTTP_200_OK, data=data)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

class OrganizerView(viewsets.ModelViewSet):
    serializer_class = serializers.OrganizerSerializer
    queryset = models.Organizer.objects.all()

class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PersonSerializer
    queryset = models.Person.objects.filter(is_blocked=False)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["first_name","last_name","email","user_type"]

    @action(detail=False, methods=['post'])
    def login(self, request):
        data=request.data
        user = self.queryset.get(email=request.data['email'])
        if user:
            if hasher.check_password(request.data['password'],user.get_password()):
                serializer = serializers.PersonSerializer(user)
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
    data = {}
    person = models.Person.objects.get(id=id)
    if request.data["user_type"] == "1":
        user = models.User.objects.get(id=person.user_id)
        address = request.data["address"]
        if address:
            serializer = serializers.UserSerializer(user,data={"address":request.data["address"]})
            if serializer.is_valid():
                serializer.save()

    elif request.data["user_type"] == "2":
        organizer = models.Organizer.objects.get(id=person.organizer_id)
        serializer = serializers.OrganizerSerializer(organizer,data={"address":request.data["address"],"experience":request.data["experience"],"organization":request.data["organization"]})
        if serializer.is_valid():
            serializer.save()

        data["errors"] = str(serializer.errors)

    if request.data.get("first_name",None):
        data["first_name"] = request.data.get("first_name",None)

    if request.data.get("last_name",None):
        data["last_name"] = request.data.get("last_name",None)

    if request.data.get("phone_no",None):
        data["phone_no"] = request.data.get("phone_no",None)

    if "image" in request.data:
        data["image"] = request.data["image"]
    else:
        data["image"] = person.image
    serializer = serializers.PersonOnlySerializer(person, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    if "errors" not in data:
        data["errors"] = str(serializer.errors)
    else:
        data["errors"] += str(serializer.errors)
    return Response(status=status.HTTP_400_BAD_REQUEST, data=data)

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.QuestionSerializer
    queryset = models.Question.objects.all().order_by("-date")
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['event']

class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AnswerSerializer
    queryset = models.Answer.objects.all()

@api_view(['GET',])
def reviewed_user_events(request,id):

    reviews = models.Review.objects.filter(user=id)
    events = []
    for review in reviews:
        event = models.Event.objects.get(id=review.get_event())
        event = event.__dict__
        del event["_state"]
        if event:
            events.append(event)

    if events:
            return Response(status=status.HTTP_200_OK, data=events)
    return Response(status=status.HTTP_200_OK, data=[])

@api_view(['GET',])
def pending_user_events(request,id):


    bookings = models.Booking.objects.filter(user= id)
    events = []
    for booking in bookings:
        if not models.Review.objects.get(event=booking.get_event(), user=id):
            event = models.Event.objects.get(event= booking.get_event()).__dict__
            del event["_state"]
            events.append(event)

    return Response(status=status.HTTP_200_OK, data=events)

