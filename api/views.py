from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from api import serializers, models
from api.serializers import PersonSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

class OrganizerView(viewsets.ModelViewSet):
    serializer_class = serializers.OrganizerSerializer
    queryset = models.Organizer.objects.all()

class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PersonSerializer
    queryset = models.Person.objects.filter(is_blocked=False)
    search_fields = ('name', 'email',)

    @action(detail=False, methods=['post'])
    def login(self, request):
        data=request.data
        print(request.data["email"])
        user = self.queryset.filter(email=request.data['email'],password=request.data['password'])
        print(user)
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST,data="Invalid Email or Password")
        else:
            serializer = PersonSerializer(user,many=True)
            print(serializer.data)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
