from django.contrib import messages
from django.shortcuts import render, redirect

from helper.fetch_all import currently_available_orders

app_name = 'foodmanApp'
# Create your views here.
from helper import session, sql, fetch_all
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


def current_order(request):
    context = {}
    if session.not_this_season(request, app_name):
        messages.info(request, 'Please Sign in first')
        return redirect('/foodman')
    foodman_id = request.session.get('id')

    if request.method == 'GET':
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
    context.update(request.session)

    context['order'] = fetch_all.current_order_by_foodman(foodman_id)
    order_id = context['order']['id']
    rest_id = fetch_all.restaurant_ID_by_order_ID(order_id)
    context['restaurant'] = fetch_all.restaurant(rest_id)
    return render(request, 'foodmanApp/current_order.html', context)


def accept_order(request):
    context = {}
    if session.not_this_season(request, app_name):
        messages.info(request, 'Please Sign in first')
        return redirect('/foodman')
    print(request.session.get('status'), 'F')
    if request.session.get('status') != 'F':
        messages.info(request, 'You are either busy or In rest.')
        return redirect('/foodman')

    if request.method == 'POST':
        order_id = request.POST.get('order')
        if order_id != '':
            try:
                foodman_id = request.session.get('id')

                cursor = sql.create_cursor()
                cursor.callproc('ORDER_PICKED', [order_id, foodman_id])
                print('Successfull')
                request.session['status'] = 'R'
            except Exception as e:
                print('the order was already picked')
                print(e)
                pass
            finally:
                cursor.close()
        print(order_id)
        messages.info(request, 'Now delivery is our motto!!!!')

    context.update(request.session)
    context['orders'] = currently_available_orders()
    print(currently_available_orders())
    return render(request, 'foodmanApp/accept_order.html', context)
