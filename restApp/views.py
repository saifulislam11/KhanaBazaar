from django.shortcuts import render


# Create your views here.


def index(request):
    context = {}
    #if request.method == 'POST':

    return render(request, 'restApp/sign_in.html', context)
