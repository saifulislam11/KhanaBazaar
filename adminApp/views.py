from django.contrib import auth, messages
from django.contrib.auth.models import User
from khanabazaar.settings import MEDIA_URL, MEDIA_ROOT, STATIC_ROOT
from django.shortcuts import render, redirect
from cx_Oracle import connect
from helper.read_write_to_file import handle_uploaded_file
from helper.sql import get_next_id
from helper.wrap_and_encode import wrap_with_in_single_quote, get_hashed_value
from helper.sql import open_connection


# Create your views here.

def index(request):
    context = {}

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)
        con = open_connection()
        c = con.cursor()
        sql = "Select * From ADMIN Where EMAIL = '%s' and PASSWORD_HASH = '%s'" % (email, password)
        print(sql)
        c.execute(sql)
        admin = c.fetchone()
        c.close()
        if admin is None:
            return render(request, 'adminApp/signIn.html', context)
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
        messages.info(request, 'YOU ARE NOT LOGGED IN ')
        request.method = 'GET'
        redirect('adminApp:index')
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        logo = request.FILES.get('restaurantLogo')
        email = request.POST.get('email')
        open_time = request.POST.get('openTime')
        close_time = request.POST.get('closeTime')
        password1 = request.POST.get('password1')
        password1 = get_hashed_value(password1)
        password2 = request.POST.get('password2')
        logo_path = None
        id = get_next_id()
        if logo is not None:
            logo_path = 'rest' + id + '.' + 'png'
            print(STATIC_ROOT+'/img/',logo_path)
            handle_uploaded_file(logo, logo_path, STATIC_ROOT+'/img/')
        else:
            logo_path = 'rest0.png'  # we will use rest0 as a default restaurant pic
        sql = "INSERT INTO RESTAURANT(ID,NAME,LOCATION,LOGO_PATH,RATING,OPEN_TIME,CLOSE_TIME,EMAIL,PASSWORD_HASH)" \
              " VALUES({id}, {name}, {location}, {logo_path}, {rating}, {open_time}, {close_time}, {email}, {password_hash})"
        sql = sql.format(
            id=wrap_with_in_single_quote(id),
            name=wrap_with_in_single_quote(name),
            location=wrap_with_in_single_quote(location),
            logo_path=wrap_with_in_single_quote(logo_path),
            rating=5.00,
            open_time=wrap_with_in_single_quote(open_time),
            close_time=wrap_with_in_single_quote(close_time),
            email=wrap_with_in_single_quote(email),
            password_hash=wrap_with_in_single_quote(password1)
        )
        print(wrap_with_in_single_quote(email))
        print(sql)
        con = open_connection()
        c = con.cursor()
        c.execute(sql)
        con.commit()
        con.close()
        messages.info(request, 'Adding Done')
        return redirect('adminApp:addRestaurant')

    return render(request, 'adminApp/addRestaurant.html', context)
