from django.http import HttpResponse
from django.shortcuts import render
import requests
events = None
# Create your views here.
def index(request):
    return render(request,'index.html')

def ajax(request):
    print("------------------------")
    print(request.GET["home"])
    return HttpResponse(events, content_type='application/json')

def tips(request):
    return render(request,'tips.html')
def faq(request):
    return render(request,'faq.html')
def specialEvent(request):
    return render(request,'special-event.html')
def tours(request):
    global events
    response = requests.get("http://127.0.0.1:8000/api/events/")
    data = response.json()
    global events
    events= { str(i["id"]) : i for i in data }
    return render(request,'all-package.html',{'data':events})

def tourDetail(request,id):
    global events
    if events:
        data = events[id]
    else:
        response = requests.get("http://127.0.0.1:8000/api/events/"+id)
        data = response.json()
    return render(request,'tour-details.html',{"data":data})

def login(request):
    return render(request,'login.html')

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