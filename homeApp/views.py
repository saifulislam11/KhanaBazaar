from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'homeApp/index.html')

def aboutus(request):
    return render(request,'homeApp/aboutus.html')
def contactus(request):
    return render(request,'homeApp/contactus.html')
