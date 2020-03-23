from rest_framework import serializers
from api import models

class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Organizer
        fields=("id","cnic","address","organization","is_verified","rating","name","email","phone")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.User
        fields = ("id", "address","name","email","phone")

class PersonSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False,allow_null=True)
    organizer = OrganizerSerializer(many=False,allow_null=True)
    class Meta:
        model=models.Person
        fields=('id','first_name','last_name','email','password','phone_no','is_blocked','image','date','user_type','user','organizer')

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

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Image
        fields="__all__"

class EventSerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=True,allow_null=True)
    organizer = OrganizerSerializer(many=False,allow_null=False)
    class Meta:
        model=models.Event
        fields=('id','title','description','date_of_departure','date_of_arrival','slots','pic','price','is_completed','is_accomodation','is_food','organizer','image')
        #fields="__all__"
    def create(self, validated_data):
        images = validated_data.pop('image',None)
        event = models.Event.objects.create(**validated_data)
        for image in images:
            models.Image.objects.create(**image,event=event)
        return event