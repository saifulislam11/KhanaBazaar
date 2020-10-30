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
    return render(request, 'adminApp/addRestaurant.html', context)
