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
        if action == 'logout' and request.session['app_name'] == app_name:
            request.session.flush()
            print('log out ing')
            return render(request, 'foodmanApp/sign_in.html', context)
        if 'status' in request.GET:
            try:
                foodman_id = request.session.get('id')
                status = request.GET.get('status')
                cursor = sql.create_cursor()
                if status != request.session.get('status'):
                    request.session['status'] = status

                    cursor.callproc('CHANGE_FOODMAN_STATUS', [foodman_id, status])
                    print('succesfully changed status')
            except Exception as e:
                print('something is problem in status updation')
                print(e)
                pass
            finally:
                cursor.close()
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
    status = request.session.get('status')
    if status == 'I' or status == 'F':
        messages.info(request, 'Please pick a order first')
        return redirect('/foodman')
    if request.method == 'GET':
        if 'status' in request.GET:
            try:
                foodman_id = request.session.get('id')
                status = request.GET.get('status')
                cursor = sql.create_cursor()
                if status != request.session.get('status'):
                    request.session['status'] = status

                    cursor.callproc('CHANGE_FOODMAN_STATUS', [foodman_id, status])
                    if status == 'F':
                        order_id = fetch_all.current_order_by_foodman(foodman_id)['id']
                        print(order_id)
                        cursor.callproc('ORDER_DELIVERED', [order_id])
                        messages.info(request, 'You have succefully completed the order!!!')
                        return redirect('/foodman')

                    print('succesfully changed status')
            except Exception as e:
                print('something is problem in status updation')
                print(e)
                pass
            finally:
                cursor.close()

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
                messages.info(request, 'order was successfully picked')
                return redirect('/foodman')
            except Exception as e:
                messages.info(request, 'some error happened')
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


def add_phone(request):
    context = {}
    if session.not_this_season(request, app_name):
        messages.info(request, 'Please Sign in first')
        return redirect('/foodman')
    foodman_id = request.session.get('id')
    if request.method == 'POST':
        try:
            phone_no = request.POST.get('phone_no')
            cursor = sql.create_cursor()
            cursor.callproc('FOODMAN_ADD_PHONE_NO', [foodman_id, phone_no])
            messages.info(request, 'successfully updated phone no ')
        except Exception as e:
            print(e)
            messages.info(request, "some error occurred")
        finally:
            try:
                cursor.close()
            except:
                pass

        pass
    context = fetch_all.foodman(foodman_id)
    return render(request, 'foodmanApp/add_phone.html', context)
