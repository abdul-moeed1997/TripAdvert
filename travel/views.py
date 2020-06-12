import json
import os
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
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
from TripAdvert.settings import EMAIL_HOST_USER

prev_url = None
user = True
# Create your views here.



def index(request):
    if "tripadvert_person_id" not in request.session:
        global prev_url
        prev_url = request.get_raw_uri()
    return render(request,'index.html')




def tips(request):
    return render(request,'tips.html')
def faq(request):
    return render(request,'faq.html')
def specialEvent(request):
    return render(request,'special-event.html')

def tours(request):
    page=request.GET.get("page",None)
    if page:
        if "tripadvert_person_id" not in request.session:
            global prev_url
            prev_url = request.get_raw_uri()
        response = requests.get("http://"+request.get_host()+"/api/events/?page="+str(page))
        data = response.json()

        if data["previous"]:
            try:
                prev = data["previous"].split("?page=")[1]
            except:
                prev="1&"+filter
        else:
            prev = data["previous"]
        if data["next"]:
            next = str(data["next"].split("?page=")[1])
        else:
            next = data["next"]
        events= { str(i["id"]) : i for i in data["results"] }
        return render(request,'all-package.html',{'data':events,'prev':prev,'next':next,'current':page,'prev_url':data["previous"],'next_url':data["next"]})
    return redirect("/travel/404/")

def tourDetail(request,id):
    if request.method=="POST":
        if request.session.get("tripadvert_person_id",None):
            requests.post("http://"+request.get_host()+"/api/questions/",{"event":request.POST["event"],"question":request.POST["question"],"user":request.session.get("tripadvert_person_id",None)})
    else:
        if "tripadvert_person_id" not in request.session:
            global prev_url
            prev_url = request.get_raw_uri()
    response = requests.get("http://"+request.get_host()+"/api/event/"+id)
    data = response.json()
    if "organizer" in data:
        data["rating"] = int(data["organizer"]["rating"])

    return render(request,'tour-details.html',{"data":data})


def logout(request):
    global user
    user=True
    if request.user.is_authenticated:
        auth.logout(request)
    if request.session.get("tripadvert_person_id",None):
        del request.session["tripadvert_person_id"]
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
        response = requests.post("http://"+request.get_host()+"/api/persons/login/",{'email':email,'password':password})
        if response.status_code == 200:
            data = (response.json())
            request.session["tripadvert_person_id"]=data["id"]
            if data["user_type"]==1:
                if data["user"] and data["user"]["id"]:
                    request.session["tripadvert_user_id"]=data["user"]["id"]
            elif data["user_type"]==2:
                request.session["tripadvert_user_id"]=data["organizer"]["id"]
            request.session["tripadvert_user_name"] = data["first_name"]
            request.session["tripadvert_user_type"] = data["user_type"]
            request.session["tripadvert_user_image"] = data["image"]

            global user,prev_url
            prev_url=None
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
    response = requests.delete("http://"+request.get_host()+"/api/user-bookings/"+str(id))
    return redirect("/travel/user/dashboard/event-booking")

def something_wrong(request):
    return render(request,'wrong.html')

def signUp(request):
    if not request.session.get("tripadvert_person_id", None):
        if request.method == "POST":
            data = {}
            data["first_name"] = request.POST["first_name"]
            data["last_name"] = request.POST["last_name"]
            data["phone_no"] = request.POST["phone_no"]
            data["user_type"] = 1
            data["email"] = request.POST["email"]
            data["password"] = request.POST["password"]
            data["address"] = request.POST["address"]
            data["organizer"] = None
            data["image"] = None

            response = requests.post("http://"+request.get_host()+"/api/persons/register/",data)
            if response.status_code == 200:
                data = response.json()

                request.session["tripadvert_person_id"] = data["id"]
                if data["user_type"] == 1:
                    request.session["tripadvert_user_id"] = data["user"]["id"]
                elif data["user_type"] == 2:
                    request.session["tripadvert_user_id"] = data["organizer"]["id"]
                request.session["tripadvert_user_name"] = data["first_name"]
                request.session["tripadvert_user_type"] = data["user_type"]
                request.session["tripadvert_user_image"] = data["image"]
                return redirect("/travel/")
        return render(request,'register.html')
    else:
        return redirect("/travel/")

def userMyProfile(request):
    if request.method == "GET":
        if "tripadvert_user_type" in request.session and request.session["tripadvert_user_type"]==1:
            response = requests.get("http://"+request.get_host()+"/api/users/"+str(request.session["tripadvert_user_id"]))
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

        person = {}
        person["user_type"] = request.session["tripadvert_user_type"]
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

        response = requests.put("http://"+request.get_host()+"/api/users/update/"+str(request.session["tripadvert_person_id"]),person)
        if response.status_code==200:
            data = response.json()
            request.session["tripadvert_user_name"] = data["first_name"]
            request.session["tripadvert_user_image"] = data["image"]

        return redirect("/travel/user/dashboard/my-profile")



def organizerMyProfile(request):
    if request.method == "GET":
        if "tripadvert_user_type" in request.session and request.session["tripadvert_user_type"]==2:
            response = requests.get("http://"+request.get_host()+"/api/organizers/"+str(request.session["tripadvert_user_id"]))
            if response.status_code==200:
                data = response.json()
                return render(request,'organizer-my-profile.html',{"data":data})
            else:
                return redirect(request,'/travel/something-wrong')

        global prev_url
        prev_url = request.get_raw_uri()
        return redirect('/travel/access-denied')

    elif request.method == "POST":
        data=request.POST
        person = {}
        person["user_type"] = request.session["tripadvert_user_type"]
        person["first_name"] = data["first_name"]
        person["last_name"] = data["last_name"]
        person["phone_no"] = data["phone"]
        person["address"] = data["address"]
        person["experience"] = data["experience"]
        person["organization"] = data["organization"]
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
        response = requests.put("http://"+request.get_host()+"/api/users/update/"+str(request.session["tripadvert_person_id"]),person)
        if response.status_code==200:
            data = response.json()
            request.session["tripadvert_user_name"] = data["first_name"]
            request.session["tripadvert_user_image"] = data["image"]

        return redirect("/travel/organizer/dashboard/my-profile")

def fblogin(request):
    global user,prev_url
    if request.user.is_authenticated:
        request.session["tripadvert_person_id"] = request.user.id
        request.session["tripadvert_user_name"] = request.user.first_name + " " + request.user.last_name
        request.session["tripadvert_user_type"] = 0
        prev_url=None
        user=False
    return redirect("/travel")

def userEventBooking(request):
    response = requests.get("http://"+request.get_host()+"/api/user-bookings?user=" + str(request.session["tripadvert_person_id"]))
    if response.status_code == 200:
        data = response.json()
    else:
        data={}
    return render(request,'user-bookings.html',{"data":data})

def fbUserEventBooking(request):
    response = requests.get("http://"+request.get_host()+"/api/user-bookings?user=" + str(request.session["tripadvert_person_id"]))
    if response.status_code == 200:
        data = response.json()
    else:
        data={}
    return render(request,'fb-user-bookings.html',{"data":data})

def OrganizerEventBooking(request):
    response = requests.get("http://"+request.get_host()+"/api/user-bookings?user=" + str(request.session["tripadvert_person_id"]))
    if response.status_code == 200:
        data = response.json()
    else:
        data={}
    return render(request,'organizer-bookings.html',{"data":data})



def contact(request):
    return render(request,'contact.html')

def not_found(request):
    return render(request, '404.html')

def book_event(request,id):
    if request.session.get("tripadvert_person_id", None):
        requests.post("http://" + request.get_host() + "/api/event-bookings/",{"event": id,"user": request.session.get("tripadvert_person_id", None)})
        return redirect("/travel/tours/?page=1")
    return redirect("/travel/login/")
def access_denied(request):
    return render(request, 'access-denied.html')


def about(request):
    return render(request, 'about.html')

def price_list(request):
    response = requests.post("http://"+request.get_host()+"/api/event/compare_events/",{"id":request.GET.get("events",None)})

    data=response.json()
    if data:
        return render(request, 'price-list.html', {'data': data})

    return redirect("/travel/something-worng/")

def organizerEventBookings(request):
    if request.session.get("tripadvert_user_type", None) and request.session.get("tripadvert_user_type", None)==2:
        response = requests.get("http://" + request.get_host() + "/api/event-bookings/?organizer="+str(request.session.get("tripadvert_user_id", None)))
        if response.status_code == 200:
            data = response.json()
            return render(request, 'organizer-event-bookings.html',{'data':data})
    return redirect("/travel/organizer/dashboard/event-bookings/")

def organizerEventSchedule(request,id):
    if request.session.get("tripadvert_user_type", None) and request.session.get("tripadvert_user_type", None)==2:
        response = requests.get("http://" + request.get_host() + "/api/event-schedule/?event="+str(id))
        if response.status_code == 200:
            data = response.json()
            return render(request, 'organizer-event-schedule.html',{'data':data,'event':id})
        else:
            return render(request, 'organizer-event-schedule.html', {})
    return redirect("/travel/access-denied/")

def organizerEventQuestions(request,id):
    if request.session.get("tripadvert_user_type", None) and request.session.get("tripadvert_user_type", None)==2:
        response = requests.get("http://" + request.get_host() + "/api/questions/?event="+str(id))
        if response.status_code == 200:
            data = response.json()
            return render(request, 'organizer-event-questions.html',{'data':data})
        else:
            return render(request, 'organizer-event-questions.html', {})
    return redirect("/travel/access-denied/")

def organizerSignUp(request):
    if not request.session.get("tripadvert_person_id", None):
        if request.method == "POST":
            data = {}
            data["first_name"] = request.POST["first_name"]
            data["last_name"] = request.POST["last_name"]
            data["phone_no"] = request.POST["phone_no"]
            data["user_type"] = 2
            data["email"] = request.POST["email"]
            data["password"] = request.POST["password"]
            data["address"] = request.POST["address"]
            data["cnic"] = request.POST["cnic"]
            data["experience"] = request.POST["experience"]
            data["organization"] = request.POST["organization"]
            data["organizer"] = None
            data["image"] = None
            response = requests.post("http://"+request.get_host()+"/api/persons/register/",data)
            if response.status_code == 200:
                data = response.json()

                request.session["tripadvert_person_id"] = data["id"]
                if data["user_type"] == 1:
                    request.session["tripadvert_user_id"] = data["user"]["id"]
                elif data["user_type"] == 2:
                    request.session["tripadvert_user_id"] = data["organizer"]["id"]
                request.session["tripadvert_user_name"] = data["first_name"]
                request.session["tripadvert_user_type"] = data["user_type"]
                request.session["tripadvert_user_image"] = data["image"]
                return redirect("/travel/")
        return render(request,'organizer_SignUp.html')
    else:
        return redirect("/travel/")

def forgotPassword(request):
    if request.method == "POST":
        if "email" in request.POST and "password" in request.POST:
            response = requests.post("http://" + request.get_host() + "/api/persons/updatePass/", {"email":request.POST["email"],"password":request.POST["password"]})
            if response.status_code == 200:
                data = response.json()
                del request.session[request.POST["email"]]
                return redirect("/travel/login")
        return redirect("/travel/something-wrong/")

    if "email" not in request.GET or "token" not in request.GET or request.GET["email"] not in request.session or request.session[request.GET["email"]]!=request.GET["token"]:
        return redirect("/travel/404/")

    return render(request,'forgot-pass.html',{"email":request.GET["email"]})


def EmailforgotPassword(request):
    if not request.session.get("tripadvert_user_type",None):
        if request.method == 'POST':
            unique_id = get_random_string(length=32)
            request.session[request.POST["email"]]=unique_id
            send_mail("Reset Password Link", "Your reset password link is: http://"+request.get_host()+"/travel/forgot-pass/?email="+request.POST["email"]+"&token="+str(unique_id),EMAIL_HOST_USER,[request.POST["email"]],fail_silently=False)
            return render(request, 'emailForgotMessage.html')
        return render(request, 'emailForgotPass.html')
    return redirect("/travel/")

def organizerMyEvents(request):
    data={}
    response=requests.get("http://"+request.get_host()+"/api/portfolio?user="+str(request.session["tripadvert_user_id"])+("&is_completed=false"))
    if response.status_code==200:
        data = response.json()
    return render(request, 'organizer-my-events.html',{"data":data})


def addEvent(request):
    if request.method == 'POST':
        data=request.POST.dict()
        if "image" in request.FILES:
            image=request.FILES['image']

            path = default_storage.save('tmp/somename.mp3', ContentFile(image.read()))
            image_data = os.path.join(settings.MEDIA_ROOT, path)
            with open(image_data, "rb") as img_file:
                my_string = base64.b64encode(img_file.read())
            is_food=False
            if request.POST["is_food"]=="1":
                is_food=True
            is_accomodation = False
            if request.POST["is_accomodation"] == "1":
                is_accomodation = True
            is_sightseeing = False
            if request.POST["is_sightseeing"] == "1":
                is_sightseeing = True

            data["pic"]=my_string
            data["organizer"]=int(request.session["tripadvert_user_id"])
            data["is_accomodation"]=is_accomodation
            data["is_food"]=is_food
            data["is_sightseeing"]=is_sightseeing
            default_storage.delete(path)
            response = requests.post("http://"+request.get_host()+"/api/events/",data)

            return redirect("/travel/organizer/dashboard/events")
    return render(request, 'organizer-add-event.html')


def deleteEvent(request,id):
    requests.delete("http://"+request.get_host()+"/api/events/"+str(id)+"/")
    return redirect("/travel/organizer/dashboard/events/")

def toggle_isFull(request,id):
    requests.put("http://"+request.get_host()+"/api/events/update/"+str(id))
    return redirect("/travel/organizer/dashboard/events/")

def toggle_isVerified(request,id):
    requests.put("http://"+request.get_host()+"/api/bookings/update/"+str(id))
    return redirect("/travel/organizer/events/bookings")

def organizerPortfolio(request):
    if request.session["tripadvert_user_type"]==2:
        response = requests.get("http://"+request.get_host()+"/api/portfolio?organizer="+str(request.session["tripadvert_user_id"])+"&is_completed=true")
        if response.status_code==200:
            data = response.json()
            return render(request, 'organizer-my-portfolio.html')
        return redirect("/travel/something-wrong/")
    return redirect("/travel/access-denied/")

def organizerPortfolioUser(request,id):
    if request.session.get("tripadvert_user_type",None):
        response = requests.get("http://" + request.get_host() + "/api/portfolio?organizer=" + str(id) + ("&is_completed=false"))
        if response.status_code == 200:
            data = response.json()
            if data:
                return render(request, 'user-my-portfolio.html', {"data": data,"organizer":id})
        return render(request, 'user-myportfolio.html', {"data": {},"organizer":id})
    return redirect("/travel/login/")

def organizerAddPhotos(request):
    if request.session.get("tripadvert_user_type",None):
        response = requests.get("http://" + request.get_host() + "/api/portfolio?organizer=" + str(id) + ("&is_completed=false"))
        if response.status_code == 200:
            data = response.json()
            if data:
                return render(request, 'organizer-portfolio-addphotos.html')
        return render(request, 'user-myportfolio.html', {"data": {},"organizer":id})
    return redirect("/travel/login/")

def organizerDetail(request,id):
    if request.session.get("tripadvert_user_type",None):
        response = requests.get("http://"+request.get_host()+"/api/persons/?organizer="+str(id))
        if response.status_code == 200:
            data = response.json()

            if len(data):
                data = data[0]
                request.session["organizer_pic"] = data["image"]
                return render(request, 'user-organizer-detail.html',{"data":data,"organizer":id})

        return render(request, 'user-organizer-detail.html',{"data":{},"organizer":id})
    return redirect("/travel/login/")


def userOrganizerEvents(request,id):
    if request.session.get("tripadvert_user_type",None):
        response = requests.get("http://"+request.get_host()+"/api/event/?organizer="+str(id))
        if response.status_code == 200:
            data = response.json()
            return render(request, 'user-organizer-events.html',{"data":data,"organizer":id})

        return render(request, 'user-organizer-events.html',{"data":[],"organizer":id})
    return redirect("/travel/login/")

def chat(request):
    return render(request,"chat.html")