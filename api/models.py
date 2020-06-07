from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from  django.contrib.auth.models import BaseUserManager

# Create your models here.

class PersonProfileManager(BaseUserManager):
    def create_user(self,email,first_name,last_name="",password=None):
        if not email:
            raise ValueError("User must have email")
        email = self.normalize_email(email)
        user = self.model(email=email,first_name=first_name,last_name=last_name,password=password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,first_name,last_name="",password=None):
        user = self.create_user(email,first_name,last_name=last_name,password=password)
        user.is_superuser=True
        user.is_staff=True
        user.user_type=3
        user.save(using=self._db)
        return user

class User(models.Model):
    address=models.CharField(max_length=255,blank=True)

    def first_name(self):
        """
        Return the mean rating from all comments
        """
        return self.user1.filter(user=self.id).values("first_name").first()["first_name"]

    def last_name(self):
        """
        Return the mean rating from all comments
        """
        return self.user1.filter(user=self.id).values("last_name").first()["last_name"]


    def email(self):
        """
        Return the mean rating from all comments
        """

        return self.user1.filter(user=self.id).values("email").first()["email"]

    def phone(self):
        """
        Return the mean rating from all comments
        """
        return self.user1.filter(user=self.id).values("phone_no").first()["phone_no"]

class Organizer(models.Model):
    cnic = models.CharField(max_length=13,blank=True,unique=True)
    address=models.CharField(max_length=255,blank=True)
    experience = models.CharField(max_length=255,blank=True)
    organization = models.CharField(max_length=100,blank=True)
    is_verified = models.BooleanField(default=False)

    def rating(self):
        """
        Return the mean rating from all comments
        """
        if self.reviews.aggregate(models.Avg('rating'))['rating__avg']:
            return self.reviews.aggregate(models.Avg('rating'))['rating__avg']
        else:
            return 0

    def first_name(self):
        """
        Return the mean rating from all comments
        """
        return self.organizer1.filter(organizer=self.id).values("first_name").first()["first_name"]

    def last_name(self):
        """
        Return the mean rating from all comments
        """
        return self.organizer1.filter(organizer=self.id).values("last_name").first()["last_name"]

    def email(self):
        """
        Return the mean rating from all comments
        """
        return self.organizer1.filter(organizer=self.id).values("email").first()["email"]

    def phone(self):
        """
        Return the mean rating from all comments
        """
        return self.organizer1.filter(organizer=self.id).values("phone_no").first()["phone_no"]
    #
    # def get_rating(self):
    #     return self.reviews.aggragate(models.Avg("rating"))["rating__avg"]

    def __str__(self):
        return str(self.id)



class Person(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=50,blank=True)
    last_name = models.CharField(max_length=50,blank=True)
    email = models.EmailField(max_length=255,unique=True,blank=True, null=True)
    username = models.CharField(max_length=255,blank=True)
    phone_no = models.CharField(max_length=11, blank=True, null=True)
    image = models.ImageField(upload_to ='uploads/users', blank=True, default="person.png")
    password = models.CharField(max_length=255,blank=True)
    user_type = models.IntegerField(default=1)
    user = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,related_name='user1')
    organizer = models.ForeignKey(Organizer,null=True,blank=True,on_delete=models.CASCADE,related_name='organizer1')
    date = models.DateField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False,null=True)
    is_staff = models.BooleanField(default=True)
    firebaseinstancetoken = models.CharField(default=None, max_length=1000, blank=True, null=True)

    objects = PersonProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','password']

    def get_password(self):
        return self.password
    def get_name(self):
        return self.first_name+" "+self.last_name






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
    title = models.CharField(max_length=255,blank=False)
    pic = models.ImageField(upload_to ='uploads/events/',null=True)
    description = models.CharField(max_length=1000,blank=False)
    category = models.CharField(max_length=20,null=True)
    is_full = models.BooleanField(default=False)
    home = models.CharField(max_length=255,null=True)
    destination = models.CharField(max_length=255,null=True)
    date_of_departure = models.DateTimeField(null=True)
    date_of_arrival = models.DateTimeField(null=True)
    date =  models.DateTimeField(auto_now_add=True)
    slots = models.IntegerField(null=False)
    price = models.IntegerField(null=False)
    is_completed = models.BooleanField(default=False)
    is_accomodation = models.BooleanField(default=False)
    is_sightseeing = models.BooleanField(default=False)
    is_food = models.BooleanField(default=False)
    accomodation_description = models.CharField(max_length=1000,blank=True,null=True)
    sightseeing_description = models.CharField(max_length=1000,blank=True,null=True)
    food_description = models.CharField(max_length=1000,blank=True,null=True)
    organizer = models.ForeignKey(Organizer, null=False,on_delete=models.CASCADE,related_name='organizer_event')

    def __str__(self):
        return self.title
    def schedule(self):
        return self.activity.filter(event=self.id).values()

    def free_slots(self):
        return (self.slots - Booking.objects.filter(event= self.id).count())

    def organizer_details(self):
        organizer = Organizer.objects.filter(id=self.organizer.id).values().first()
        organizer["name"]=Person.objects.filter(organizer = self.organizer.id).first().get_name()
        organizer["rating"] = Review.objects.filter(organizer=organizer["id"]).all().aggregate(models.Avg('rating'))['rating__avg']

        return organizer

    def get_id(self):
        return self.id



class EventSchedule(models.Model):
    day = models.CharField(max_length=50,blank=True)
    short_description = models.CharField(max_length=100,blank=True)
    detail_description = models.CharField(max_length=255, blank=True)
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name="activity")


class Image(models.Model):
    image = models.ImageField(upload_to ='uploads/events/',null=True)
    event = models.ForeignKey(Event,null=False,on_delete=models.CASCADE,related_name='image')


class Notification(models.Model):
    description = models.CharField(max_length=255,blank=False)
    date = models.DateTimeField(auto_now_add=True)
    sentBy = models.ForeignKey(Person, null=False,on_delete=models.CASCADE,related_name='NotificationSender')
    sentFor = models.ForeignKey(Person, null=False,on_delete=models.CASCADE,related_name='NotificationReceiver')

class Booking(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, null=False, on_delete=models.CASCADE,related_name="event_booking")
    is_verified = models.BooleanField(default=False)
    user = models.ForeignKey(Person, null=False, on_delete=models.CASCADE,related_name="user_booking")

    def event_details(self):
        return Event.objects.filter(id=self.event.id).values().first()

    def get_event(self):
        return self.event.get_id()

class Comment(models.Model):
    comment=models.CharField(max_length=255,blank=True)
    date = models.DateTimeField(auto_now_add=True,null=True)
    event = models.ForeignKey(Event, null=True,on_delete=models.CASCADE)
    user = models.ForeignKey(Person, null=False,on_delete=models.CASCADE)


class Question(models.Model):
    question=models.CharField(max_length=255,blank=True)
    date = models.DateTimeField(auto_now_add=True,null=True)
    event = models.ForeignKey(Event, null=True,on_delete=models.CASCADE)
    user = models.ForeignKey(Person, null=False,on_delete=models.CASCADE)

    def answer(self):
        answer = Answer.objects.filter(question=self.id).values().first()
        if answer:
            answer=answer["answer"]
        return answer

class Answer(models.Model):
    answer=models.CharField(max_length=255,blank=True)
    date = models.DateTimeField(auto_now_add=True,null=True)
    question = models.ForeignKey(Question, null=True,on_delete=models.CASCADE)
    organizer = models.ForeignKey(Person, null=False,on_delete=models.CASCADE)

class Review(models.Model):
    rating = models.IntegerField(null=False)
    comment = models.CharField(max_length=255, blank=True, null= True)
    date = models.DateTimeField(auto_now_add=True,null=True)
    user = models.ForeignKey(Person, null=True,on_delete=models.SET_NULL,default=None)
    organizer = models.ForeignKey(Organizer, null=False,on_delete=models.CASCADE,related_name="reviews")
    event = models.ForeignKey(Event,on_delete=models.CASCADE)

    def get_event(self):
        return self.event.get_id()