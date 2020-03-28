import os

from django import template
from django.contrib.auth import authenticate
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from django.contrib import auth
import base64

# global variables
from django.template import context

from TripAdvert import settings

events = None
prev_url = None
user = True
# Create your views here.



def index(request):
    global prev_url


    prev_url = request.get_raw_uri()
    return render(request,'index.html')


# def user_profile(request):
#     if "tripadvert_user_type" in request.session and request.session["tripadvert_user_type"]==1:
#         response = requests.get("http://127.0.0.1:8000/api/users/"+str(request.session["tripadvert_user_id"]))
#         if response.status_code==200:
#             data = response.json()
#             return render(request,'user-my-profile.html',{"data":data})
#         else:
#             return redirect(request,'/travel/something-wrong')
#     elif "tripadvert_user_type" in request.session and request.session["tripadvert_user_type"]==2:
#         response = requests.get("http://127.0.0.1:8000/api/organizers/" + str(request.session["tripadvert_user_id"]))
#         if response.status_code == 200:
#             data = response.json()
#             return render(request, 'organizer-my-profile.html', {"data": data})
#         else:
#             return redirect(request, '/travel/something-wrong')
#
#
#     global prev_url
#     prev_url = request.get_raw_uri()
#     return redirect('/travel/access-denied')

def ajax(request):
    return HttpResponse(events, content_type='application/json')

def tips(request):
    return render(request,'tips.html')
def faq(request):
    return render(request,'faq.html')
def specialEvent(request):
    return render(request,'special-event.html')
def tours(request):
    global prev_url
    prev_url = request.get_raw_uri()
    global events
    response = requests.get("http://127.0.0.1:8000/api/events/")
    data = response.json()
    global events
    events= { str(i["id"]) : i for i in data }
    return render(request,'all-package.html',{'data':events})

def tourDetail(request,id):
    global prev_url
    prev_url = request.get_raw_uri()
    global events
    if events:
        data = events[id]
    else:
        response = requests.get("http://127.0.0.1:8000/api/event/"+id)
        data = response.json()
    return render(request,'tour-details.html',{"data":data})


def logout(request):
    global user
    user=True
    if request.user.is_authenticated:
        auth.logout(request)
    if request.session.get("tripadvert_user_name",None):
        del request.session["tripadvert_user_name"]
    if request.session.get("tripadvert_user_type", None):
        del request.session["tripadvert_user_type"]
    if request.session.get("tripadvert_user_id", None):
        del request.session["tripadvert_user_id"]
    return redirect("/")

def login(request):
    global prev_url
    data=""
    if request.method=='POST':
        email = request.POST["email"]
        password = request.POST["password"]
        response = requests.post("http://127.0.0.1:8000/api/persons/login/",{'email':email,'password':password})
        if response.status_code == 200:
            data = (response.json()[0])
            request.session["tripadvert_person_id"]=data["id"]
            if data["user_type"]==1:
                request.session["tripadvert_user_id"]=data["user"]["id"]
            elif data["user_type"]==2:
                request.session["tripadvert_user_id"]=data["organizer"]["id"]
            request.session["tripadvert_user_name"] = data["first_name"]
            request.session["tripadvert_user_type"] = data["user_type"]
            request.session["tripadvert_user_image"] = data["image"]

            global user
            user=False
            if prev_url:
                temp_url = prev_url
                prev_url = None
            else:
                temp_url='Home'
            return redirect(temp_url)
        elif response.status_code == 400:
            data = response.json()

    return render(request,'login.html',{"data":data})


def deleteBooking(request,id):
    response = requests.delete("http://127.0.0.1:8000/api/user-bookings/"+str(id))
    return redirect("/travel/user/dashboard/event-booking")

def something_wrong(request):
    return render(request,'wrong.html')

def signUp(request):
    return render(request,'register.html')

def userMyProfile(request):
    if request.method == "GET":
        if "tripadvert_user_type" in request.session and request.session["tripadvert_user_type"]==1:
            response = requests.get("http://127.0.0.1:8000/api/users/"+str(request.session["tripadvert_user_id"]))
            if response.status_code==200:
                data = response.json()
                return render(request,'user-my-profile.html',{"data":data})
            else:
                return redirect(request,'/travel/something-wrong')

        global prev_url
        prev_url = request.get_raw_uri()
        return redirect('/travel/access-denied')

    elif request.method == "POST":
        data=request.POST
        person = requests.get("http://127.0.0.1:8000/api/persons/"+str(request.session["tripadvert_person_id"])+"/")
        person = person.json()
        person["user"]=int(person["user"]["id"])
        person["organizer"]=None
        person["first_name"] = data["first_name"]
        person["last_name"] = data["last_name"]
        person["phone_no"] = data["phone"]
        person["address"] = data["address"]
        if "image" in request.FILES:
            image=request.FILES['image']

            path = default_storage.save('tmp/somename.mp3', ContentFile(image.read()))
            image_data = os.path.join(settings.MEDIA_ROOT, path)
            with open(image_data, "rb") as img_file:
                my_string = base64.b64encode(img_file.read())
            person['image'] = my_string
            default_storage.delete(path)
        else:
            del person['image']
        response = requests.put("http://127.0.0.1:8000/api/users/update/"+str(request.session["tripadvert_person_id"]),person)
        if response.status_code==200:
            data = response.json()
            request.session["tripadvert_user_name"] = data["first_name"]
            request.session["tripadvert_user_image"] = data["image"]

        return redirect("/travel/user/dashboard/my-profile")

def fblogin(request):
    global user
    if request.user.is_authenticated:
        request.session["tripadvert_person_id"] = request.user.id
        request.session["tripadvert_user_name"] = request.user.first_name + " " + request.user.last_name
        request.session["tripadvert_user_type"] = 0
        user=False
    return redirect("/travel")

def eventBooking(request):
    response = requests.get("http://127.0.0.1:8000/api/user-bookings?user=" + str(request.session["tripadvert_person_id"]))
    if response.status_code == 200:
        data = response.json()
    else:
        data={}
    return render(request,'user-bookings.html',{"data":data})

def userEditProfile(request):
    return render(request,'edit-profile.html')

def contact(request):
    return render(request,'contact.html')

def not_found(request):
    return render(request, '404.html')

def access_denied(request):
    return render(request, 'access-denied.html')


def about(request):
    return render(request, 'about.html')

def price_list(request):
    return render(request, 'price-list.html')

def eventBookingDetails(request):
    return render(request,'eventBookingDetails.html')

def organizerSignUp(request):
    return render(request,'organizer_SignUp.html')

def forgotPassword(request):
    return render(request,'forgot-pass.html')


def EmailforgotPassword(request):
    return render(request, 'emailForgotPass.html')


def organizerProfile(request):
    return render(request, 'organizerProfile.html')


def editProfileOrganizer(request):
    return render(request, 'editProfileOrg.html')


def organizerEvents(request):
    return render(request, 'orgEvents.html')


def addEvent(request):
    return render(request, 'add-event.html')


def organizerPortfolio(request):
    return render(request, 'my-portfolio.html')

def organizerPortfolioUser(request):
    return render(request, 'my-portfolio-user.html')


def organizerDetail(request):
    return render(request, 'organizer-detail.html')