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
    queryset = models.Booking.objects.filter(event__is_completed=False)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['user']


class PortfolioViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PortfolioSerializer
    queryset = models.Event.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['organizer','is_completed']

class EventBookingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BookingSerializer
    queryset = models.Booking.objects.filter(event__is_full=False).order_by("is_verified","date")
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['event']

    def get_queryset(self):
        organizer = self.request.query_params.get('organizer',None)
        if organizer:
            queryset = models.Booking.objects.filter(event__organizer=organizer,event__is_full=False).order_by("is_verified","date")
        else:
            queryset = models.Booking.objects.filter(event__is_full=False).order_by("is_verified","date")
        return queryset


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventScheduleSerializer
    queryset = models.EventSchedule.objects.all().order_by("id")
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['event']

class PersonOnlyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PersonOnlySerializer
    queryset = models.Person.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['email']

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

    @action(detail=False, methods=['get'])
    def top_events(self, request):
        newlist = []
        serializer = serializers.SingleEventSerializer(self.queryset, many=True)
        if serializer.data:
            newlist = sorted(serializer.data, key=lambda k: k['free_slots'])[:10]
        return Response(status=status.HTTP_200_OK, data=newlist)


class SingleEventViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SingleEventSerializer
    queryset = models.Event.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['organizer']
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
    filterset_fields = ["first_name","last_name","email","user_type","organizer"]

    @action(detail=False, methods=['get'])
    def top_organizers(self, request):
        newlist = []
        organizers = self.queryset.filter(user_type=2)
        serializer = serializers.PersonSerializer(organizers,many=True)
        if serializer.data:
            newlist = sorted(serializer.data, key=lambda k: k['organizer']['rating'])[:10]
        return Response(status=status.HTTP_200_OK, data=newlist)

    @action(detail=False, methods=['post'])
    def updatePass(self, request):
        if request.data.get("email",None) and request.data.get("password",None):
            person = models.Person.objects.get(email=request.data.get("email",None))
            new = make_password(request.data.get("password",None))
            person.password = new
            person.save()
            serializer = serializers.PersonSerializer(person)
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST, data = [])
    @atomic
    @action(detail=False, methods=['post'])
    def register(self, request):
        data = (request.data).dict()
        person = models.Person()
        person.first_name = data["first_name"]
        person.last_name = data["last_name"]
        person.phone_no = data["phone_no"]
        person.email = data["email"]
        person.image = None
        person.password = make_password(data["password"])
        if data["user_type"] == '1':
            user = models.User()
            person.user_type = 1
            user.address = data["address"]
            user.save()
            person.user_id = user.id
            person.organizer_id = None
        elif data["user_type"] == '2':
            organizer = models.Organizer()
            person.user_type = 2
            organizer.address = data["address"]
            organizer.organization = data["organization"]
            organizer.experience = data["experience"]
            organizer.cnic = data["cnic"]
            organizer.save()
            person.organizer_id = organizer.id
            person.user_id = None

        person.save()
        serializer = serializers.PersonSerializer(person)
        return Response(status=status.HTTP_200_OK, data = serializer.data)

    @action(detail=False, methods=['post'])
    def login(self, request):
        data=request.data
        user = self.queryset.get(email=request.data['email'])
        if user.user_id or user.organizer_id:
            if user:
                if hasher.check_password(request.data['password'],user.get_password()):
                    serializer = serializers.PersonSerializer(user)
                    return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="This Email is registered as Social Login! Please use Social login option")
        return Response(status=status.HTTP_400_BAD_REQUEST,data="Invalid Email or Password!")

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
def toggle_isVerified(request,id):
    booking = models.Booking.objects.get(id=id)
    if booking:
        if booking.is_verified:
            booking.is_verified=False
        else:
            booking.is_verified=True
        booking.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT',])
@atomic
def update_user(request,id):
    data = {}
    person = models.Person.objects.get(id=id)
    if person:
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
            if person.image:
                image = str(person.image)
                path = "media\\uploads\\users\\" + image.split("/")[-1]
                os.remove(path)
            data["image"] = request.data["image"]
        else:
            data["image"] = person.image

        serializer = serializers.PersonOnlySerializer(person, data=data)
        if serializer.is_valid():
            person = serializer.save()
            serializer = serializers.PersonSerializer(person)
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        if "errors" not in data:
            data["errors"] = str(serializer.errors)
        else:
            data["errors"] += str(serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
    return Response(status=status.HTTP_400_BAD_REQUEST,data = {})

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
        if event:
            event = event.__dict__
            del event["_state"]
            event["organizer"] = event["organizer_id"]
            del event["organizer_id"]
            if event not in events:
                events.append({"event":event,"rating": review.rating})

    if events:
            return Response(status=status.HTTP_200_OK, data=events)
    return Response(status=status.HTTP_200_OK, data=[])

@api_view(['GET',])
def pending_user_events(request,id):

    bookings = models.Booking.objects.filter(user= id)
    events = []
    for booking in bookings:

        if not models.Review.objects.filter(event=booking.get_event(), user=id,event__event_booking__is_verified=True):
            event = models.Event.objects.get(id= booking.get_event(), is_completed= True)
            if event:
                event = event.__dict__
                del event["_state"]
                event["organizer"] = event["organizer_id"]
                del event["organizer_id"]
                if event not in events:
                    events.append({"event":event,"rating": None})

    return Response(status=status.HTTP_200_OK, data=events)

@api_view(['POST',])
def setFirebaseInstanceToken(request,id):
    person = models.Person.objects.get(id=id)

    if person:
        data = {}
        person.firebaseinstancetoken = request.data.get("firebase_token",None)
        person.save()
        serializer = serializers.PersonSerializer(person)

        return Response(status=status.HTTP_200_OK, data=serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST, data=[])
