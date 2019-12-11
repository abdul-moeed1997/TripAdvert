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
def profile(request):
    return render(request,'profile.html')
def eventBooking(request):
    return render(request,'eventBooking.html')
def editProfile(request):
    return render(request,'edit-Profile.html')
def contact(request):
    return render(request,'contact.html')
