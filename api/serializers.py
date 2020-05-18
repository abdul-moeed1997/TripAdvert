from django.contrib.auth.hashers import make_password
from django.http.multipartparser import MultiPartParser
from rest_framework import serializers
from api import models


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Organizer
        fields=("id","cnic","address","organization","experience","is_verified","rating","first_name","last_name","email","phone")

class SimpleOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Organizer
        fields=("id","cnic","address","organization","experience","is_verified","rating")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.User
        fields = ("id", "address","first_name","last_name","email","phone")
class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.User
        fields = ("id", "address")

class PersonSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)
    user = SimpleUserSerializer(many=False,allow_null=True)
    organizer = SimpleOrganizerSerializer(many=False,allow_null=True)
    class Meta:
        model=models.Person
        fields=('id','first_name','last_name','email','password','phone_no','is_blocked','image','date','user_type','user','organizer')

    def create(self, validated_data):
        if 'username' not in validated_data:
            validated_data['username'] = validated_data['email']
        validated_data['password'] = make_password(validated_data.get('password'))
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


class EventScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventSchedule
        fields="__all__"

class EventSerializer(serializers.ModelSerializer):
    pic = Base64ImageField(max_length=None, use_url=True)
    class Meta:
        model=models.Event
        fields=('id','title','description','home','destination','category','date','date_of_departure','date_of_arrival','slots','pic','price','is_completed','is_accomodation','accomodation_description','is_food','food_description','is_sightseeing','sightseeing_description','organizer','organizer_details')


class PortfolioSerializer(serializers.ModelSerializer):
    pic = Base64ImageField(max_length=None, use_url=True)
    class Meta:
        model=models.Event
        fields = "__all__"

class SingleEventSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer(many=False,read_only=True)
    class Meta:
        model=models.Event
        fields=('id','title','description','date','date_of_departure','date_of_arrival','slots','pic','price','is_completed','is_accomodation','accomodation_description','is_food','food_description','is_sightseeing','sightseeing_description','organizer','schedule')



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Booking
        fields=('id','is_verified','user','event','event','event_details')


class PersonOnlySerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)
    class Meta:
        model=models.Person
        fields=('id','first_name','last_name','phone_no','is_blocked','image','date','user_type','user','organizer')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Question
        fields=('id','question','date','event','user','answer')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Answer
        fields=('id','answer','date','organizer','question')

