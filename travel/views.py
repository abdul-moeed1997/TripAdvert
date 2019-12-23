from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

def tips(request):
    return render(request,'tips.html')
def faq(request):
    return render(request,'faq.html')
def specialEvent(request):
    return render(request,'special-event.html')
def tours(request):
    return render(request,'all-package.html')

def tourDetail(request):
    return render(request,'tour-details.html')

def login(request):
    return render(request,'login.html')

def signUp(request):
    return render(request,'register.html')

def myProfile(request):
    return render(request,'my-profile.html')

def dashboard(request):
    return render(request,'dashboard.html')

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