from django.shortcuts import render, redirect
from cx_Oracle import connect

loggedIn = False


def openConnection():
    con = connect("KB", "123", "localhost/orcl")
    return con


# Create your views here.

def index(request):
    global loggedIn
    context = {}
    if loggedIn:
        return render(request,'adminApp/index.html', context)
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)
        con = openConnection()
        c = con.cursor()
        sql = "Select * From ADMIN Where EMAIL = '%s' and PASSWORD_HASH = '%s'" % (email, password)
        print(sql)
        c.execute(sql)
        admin = c.fetchone()
        if admin is None:
            return redirect('adminApp/',context)
        else:
            print('We need to do something')
            loggedIn = True
            return render(request, 'adminApp/index.html',context)
    else:
        return render(request, 'adminApp/signIn.html',context)


def addRestaurant(request):
    context = {}
    global loggedIn
    # if not loggedIn:
    #     request.method = 'GET'
    #     return index(request)

    if request.method == 'POST':
        print(request.FILES)
        name = request.POST.get('name')
        location = request.POST.get('location')
        logo = request.FILES['restaurantLogo']
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(logo)
        return redirect('adminApp:addRestaurant')

    return render(request, 'adminApp/addRestaurant.html', context)
