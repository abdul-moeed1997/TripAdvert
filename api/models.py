from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from  django.contrib.auth.models import BaseUserManager

# Create your models here.

class PersonProfileManager(BaseUserManager):
    def create_user(self,email,name,password=None):
        if not email:
            raise ValueError("User must have email")
        email = self.normalize_email(email)
        user = self.model(email=email,name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,name,password):
        user = self.create_user(email,name,password)
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user

class User(models.Model):
    address=models.CharField(max_length=255,blank=True)

class Organizer(models.Model):
    cnic = models.CharField(max_length=13,blank=True,unique=True)
    address=models.CharField(max_length=255,blank=True)
    experience = models.CharField(max_length=255,blank=True)
    organization = models.CharField(max_length=100,blank=True)
    is_verified = models.BooleanField(default=False)


class Person(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255,unique=True)
    phone_no = models.CharField(max_length=11)
    image = models.ImageField(upload_to ='uploads/',null=True)
    password = models.CharField(max_length=50)
    user_type = models.IntegerField(default=1)
    user = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    organizer = models.ForeignKey(Organizer,null=True,blank=True,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False,null=True)


    objects = PersonProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','password']


class Review(models.Model):
    rating = models.IntegerField(null=False)
    comment=models.CharField(max_length=255,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=False,on_delete=models.CASCADE)
    organizer = models.ForeignKey(Organizer, null=False,on_delete=models.CASCADE)


class BlockRequest(models.Model):
    reason = models.CharField(max_length=255,blank=False)
    proof=models.ImageField(null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    sentBy = models.ForeignKey(Person, null=False,on_delete=models.CASCADE,related_name='RequestBy')
    sentFor = models.ForeignKey(Person, null=False,on_delete=models.CASCADE,related_name='RequestFor')

class Message(models.Model):
    message = models.CharField(max_length=255,blank=False)
    date = models.DateTimeField(auto_now_add=True)
    sentBy = models.ForeignKey(Person, null=False,on_delete=models.CASCADE,related_name='MessageSender')
    sentFor = models.ForeignKey(Person, null=False,on_delete=models.CASCADE,related_name='MessageReceiver')

class Event(models.Model):
    name = models.CharField(max_length=255,blank=False)
    description = models.CharField(max_length=1000,blank=False)
    date_of_departure = models.DateTimeField(null=False)
    date_of_arrival = models.DateTimeField(null=False)
    slots = models.IntegerField(null=False)
    is_completed = models.BooleanField(default=False)
    is_accomodation = models.BooleanField(default=False)
    is_food = models.BooleanField(default=False)
    accomodation_description = models.CharField(max_length=1000,blank=True,null=True)
    food_description = models.CharField(max_length=1000,blank=True,null=True)
    organizer = models.ForeignKey(Organizer, null=False,on_delete=models.CASCADE,related_name='organizer')

class Image(models.Model):
    image = models.ImageField(null=False)
    event = models.ForeignKey(Event,null=False,on_delete=models.CASCADE)


class Notification(models.Model):
    description = models.CharField(max_length=255,blank=False)
    date = models.DateTimeField(auto_now_add=True)
    sentBy = models.ForeignKey(Person, null=False,on_delete=models.CASCADE,related_name='NotificationSender')
    sentFor = models.ForeignKey(Person, null=False,on_delete=models.CASCADE,related_name='NotificationReceiver')

class Booking(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)