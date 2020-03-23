from django import template
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from django.contrib import auth


# global variables
from django.template import context

events = None
prev_url = None
user = True
# Create your views here.



def index(request):
    global prev_url, user
    if request.user.is_authenticated and user:
        request.session["tripadvert_user_id"] = request.user.id
        request.session["tripadvert_user_name"] = request.user.first_name
        request.session["tripadvert_user_type"] = 0
        user=False

    if request.session.get("tripadvert_user_type")==0:
        print("=-=-=-=-=-=-")
    prev_url = request.get_raw_uri()
    return render(request,'index.html')


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
        response = requests.get("http://127.0.0.1:8000/api/events/"+id)
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
            request.session["tripadvert_user_id"]=data["id"]
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

def signUp(request):
    return render(request,'register.html')

def myProfile(request):
    return render(request,'my-profile.html')


def eventBooking(request):
    return render(request,'eventBooking.html')

def editProfile(request):
    return render(request,'edit-Profile.html')

def contact(request):
    return render(request,'contact.html')

def not_found(request):
    return render(request, '404.html')
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