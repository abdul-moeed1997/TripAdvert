from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')
def signUp(request):
    return render(request,'register.html')
def profile(request):
    return render(request,'profile.html')
