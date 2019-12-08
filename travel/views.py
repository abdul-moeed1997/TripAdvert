from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

def tours(request):
    return render(request,'all-package.html')

def tourDetail(request):
    return render(request,'tour-details.html')
