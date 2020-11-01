from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from cx_Oracle import connect
from helper.read_write_to_file import handle_uploaded_file
from helper.sql import get_next_id
from khanabazaar.settings import MEDIA_URL, MEDIA_ROOT
from helper.sql import openConnection




# Create your views here.

def index(request):
    context = {}

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)
        con = openConnection()
        c = con.cursor()
        sql = "Select * From ADMIN Where EMAIL = '%s' and PASSWORD_HASH = '%s'" % (email, password)
        print(sql)
        c.execute(sql)
        admin = c.fetchone()
        c.close()
        if admin is None:
            return render(request,'adminApp/signIn.html',context)
        else:
            print('We need to do something')
            print(type(request.session))
            request.session['email'] = email
            for r in request.session.items():
                print(r)
            # user = auth.authenticate(usename=email, password=password, email=email)
            # user = User.objects.create_user(username=email,email=email, password=password)
            return render(request, 'adminApp/index.html', context)
    else:
        return render(request, 'adminApp/signIn.html', context)


def addRestaurant(request):
    context = {}
    for r in request.session.items():
        print(r)
    if request.session.is_empty():
        messages.info(request,'YOU ARE NOT LOGGED IN ')
        request.method = 'GET'
        redirect('adminApp:index')
    if request.method == 'POST':
        print(request.FILES)
        name = request.POST.get('name')
        location = request.POST.get('location')
        logo = request.FILES.get('restaurantLogo')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(logo)
        id = get_next_id()
        if logo is not None:
            handle_uploaded_file(logo, 'rest', MEDIA_ROOT, id)
        messages.info(request, 'Adding Done')
        return redirect('adminApp:addRestaurant')

    return render(request, 'adminApp/addRestaurant.html', context)
