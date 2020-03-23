from django.contrib import auth
from django.contrib.auth.hashers import make_password
import django.contrib.auth.hashers as hasher
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

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



class SessionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SessionSerializer
    queryset = models.SessionLogin.objects.all()

class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ImageSerializer
    queryset = models.Image.objects.all()

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.filter(is_completed=False)



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


