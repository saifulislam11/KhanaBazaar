from django.contrib import messages
from django.shortcuts import render

from helper import sql
from helper.wrap_and_encode import get_hashed_value, wrap_with_in_single_quote


# Create your views here.


def index(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password = get_hashed_value(password)
        c = sql.create_cursor()
        to_execute = "SELECT * FROM RESTAURANT WHERE EMAIL ={email} AND PASSWORD_HASH ={password}"
        # print(to_execute)

        to_execute = to_execute.format(
            email=wrap_with_in_single_quote(email),
            password=wrap_with_in_single_quote(password)
        )
        c.execute(to_execute)
        foodman = c.fetchone()
        c.close()
        if foodman is None:
            messages.info(request, 'Please provide correct information')
            return render(request, 'restApp/sign_in.html', context)
        else:
            pass

    return render(request, 'restApp/sign_in.html', context)
