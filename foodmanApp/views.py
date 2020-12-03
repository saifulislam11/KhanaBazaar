from django.contrib import messages
from django.shortcuts import render

app_name = 'foodmanApp'
# Create your views here.
from helper import session, sql
from helper.wrap_and_encode import wrap_with_in_single_quote, get_hashed_value


def index(request):
    context = {}
    session.not_this_season(request, app_name)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email != '' and password != '':
            try:
                password = get_hashed_value(password)
                cursor = sql.create_cursor()
                to_execute = "SELECT * FROM FOODMAN WHERE EMAIL = {email} AND PASSWORD_HASH = {password}"
                to_execute = to_execute.format(
                    email=wrap_with_in_single_quote(email),
                    password=wrap_with_in_single_quote(password)
                )
                cursor.execute(to_execute)
                row = cursor.fetchone()
                if row is None:
                    messages.info(request, "Incorrect credintials")
                    return render(request, 'foodmanApp/sign_in.html', context)
                else:
                    request.session['app_name'] = app_name
                    request.session['id'] = row[0]
                    request.session['name'] = row[1]

                    request.session['location'] = row[6]
                    request.session['image_path'] = row[5]
                    request.session['status'] = row[7]
                    context.update(request.session)
                    # print(context)
                    return render(request, 'foodmanApp/index.html', context)
            except Exception as e:
                print(e)
                messages.info(request, 'Some error occured!!! please Try again!!!')
                return render(request, 'foodmanApp/sign_in.html', context)
                pass
            finally:
                cursor.close()
        else:
            messages.info(request, "Incorrect credintials")
            return render(request, 'foodmanApp/sign_in.html', context)

    elif request.method == 'GET':
        action = request.GET.get('action')
        if action == 'logout':
            request.session.flush()
            print('log out ing')
            return render(request, 'foodmanApp/sign_in.html', context)
        if 'location' in request.GET:
            try:
                foodman_id = request.session.get('id')
                location = request.GET.get('location')
                if location != request.session.get('location'):
                    request.session['location'] = location
                    to_execute = "UPDATE FOODMAN SET LOCATION = {location} WHERE ID = {id}"
                    to_execute = to_execute.format(
                        location=wrap_with_in_single_quote(location),
                        id=wrap_with_in_single_quote(foodman_id)
                    )
                    sql.execute(to_execute)
                    print(to_execute)
            except Exception as e:
                print(e)
                pass
        else:
            print('why location is not being updated')

        if not request.session.is_empty():
            context.update(request.session)
            print(context)
            return render(request, 'foodmanApp/index.html', context)
        else:
            return render(request, 'foodmanApp/sign_in.html', context)

    # return render(request, 'foodmanApp/sign_in.html', context)
