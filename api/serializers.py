from rest_framework import serializers
from api import models

class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Organizer
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.User
        fields="__all__"

class PersonSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False,allow_null=True)
    organizer = OrganizerSerializer(many=False,allow_null=True)
    class Meta:
        model=models.Person
        fields=('id','name','email','password','phone_no','is_blocked','image','date','user_type','user','organizer')

    def create(self, validated_data):
        user = validated_data.pop('user',None)
        organizer = validated_data.pop('organizer',None)
        user_type = validated_data.get('user_type',None)
        if user_type==1 :
            userID = models.User.objects.create(**user)
        else:
            userID=None
        if user_type==2:
            organizerID = models.Organizer.objects.create(**organizer)
        else:
            organizerID=None
        person = models.Person.objects.create(**validated_data,user=userID,organizer=organizerID)
        return person
