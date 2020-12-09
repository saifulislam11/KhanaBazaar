from django.contrib import messages
from django.shortcuts import render, redirect

from helper import sql, fetch_all
from helper.location import valid_location, buet_location
from helper.read_write_to_file import handle_uploaded_file
from helper.session import not_this_season
from helper.wrap_and_encode import get_hashed_value, wrap_with_in_single_quote
from khanabazaar.settings import STATIC_ROOT, IMAGE_PATH
from restApp.urls import app_name


def index(request):
    context = {}
    not_this_season(request, app_name)
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
        rest = c.fetchone()
        c.close()
        if rest is None:
            messages.info(request, 'Please provide correct information')
            return render(request, 'restApp/sign_in.html', context)
        else:
            id = rest[0]
            name = rest[1]
            location = rest[2]
            if not valid_location(location):
                location = buet_location

            email = rest[7]
            # password = rest[8]
            request.session['id'] = id
            request.session['user_name'] = name
            request.session['email'] = email
            request.session['location'] = location
            request.session['app_name'] = app_name
            context['user_name'] = request.session.get('user_name')
            return render(request, 'restApp/index.html', context)

    elif request.method == 'GET':
        action = request.GET.get('action')
        if action == 'logout':
            request.session.flush()
            print('log out ing')
            return render(request, 'restApp/sign_in.html', context)

        if not request.session.is_empty():
            context['user_name'] = request.session.get('user_name')
            return render(request, 'restApp/index.html', context)
        else:
            return render(request, 'restApp/sign_in.html', context)

    return render(request, 'restApp/sign_in.html', context)


def add_food(request):
    context = {}
    if not_this_season(request, app_name):
        messages.info(request, 'Please log in')
        return redirect('/rest')
    if request.method == 'POST':

        try:
            name = request.POST.get('name')
            image = request.FILES['food_image']
            price = request.POST.get('price')
            description = request.POST.get('description')
            food_id = sql.get_next_id()
            rest_id = request.session.get('id')
            Type = request.POST.get('type')
            image_id = 0
            # this are default
            available = 'N'
            offer = 0
            food_image_path = None

            conn = sql.open_connection()
            cursor = conn.cursor()
            # first add to fooditem table
            to_execute = "INSERT INTO FOOD_ITEM(ID, RESTAURANT_ID, NAME, PRICE,OFFER, AVAILIBILITY, DESCRIPTION, TYPE) " \
                         "VALUES ({id}, {rest_id}, {name},{price}, {offer}, {availibiliy}, {description}, {type} )"
            to_execute = to_execute.format(
                id=wrap_with_in_single_quote(food_id),
                rest_id=wrap_with_in_single_quote(rest_id),
                name=wrap_with_in_single_quote(name),
                price=price,
                offer=offer,
                availibiliy=wrap_with_in_single_quote(available),
                description=wrap_with_in_single_quote(description),
                type=wrap_with_in_single_quote(Type)
            )
            # print(to_execute)
            cursor.execute(to_execute)

            # now add to food item path
            if image is not None:
                image_id = sql.get_next_id()
                food_image_path = 'food' + image_id + '.jpg'
                handle_uploaded_file(image, food_image_path, STATIC_ROOT + '/img')
                handle_uploaded_file(image, food_image_path, IMAGE_PATH + '/img/')
            else:
                food_image_path = 'food' + image_id + '.jpg'

            to_execute = "INSERT INTO FOOD_ITEM_PATH(ID, IMAGE_PATH) VALUES ( {id}, {food_path})"
            to_execute = to_execute.format(
                id=wrap_with_in_single_quote(food_id),
                food_path=wrap_with_in_single_quote(food_image_path)
            )
            cursor.execute(to_execute)
            cursor.close()
            conn.commit()
            messages.info(request, 'Successfully added Food')

        except Exception as e:
            print(e)
            print("something is wrong in adding food")
            print(e)
            messages.info(request, 'some error occured!')
            try:
                conn.rollback()
            except:
                pass
        finally:
            try:
                conn.close()
            except:
                pass

    return render(request, 'restApp/add_food.html', context)


def edit_food(request):
    context = {}
    if not_this_season(request, app_name):
        messages.info(request, 'Please log in')
        return redirect('/rest')
    if request.method == 'GET':

        if not request.session.is_empty():
            rest_id = request.session.get('id')
            context['foods'] = fetch_all.food_item_all(rest_id)
            return render(request, 'restApp/edit_food.html', context)

    return render(request, 'restApp/edit_food.html', context)


def edit_particular_food(request):
    context = {}
    if not_this_season(request, app_name):
        messages.info(request, 'Please log in')
        return redirect('/rest')
    rest_id = request.session.get('id')
    if request.method == 'GET':
        # print(request.GET)
        food_id = request.GET.get('food_id')
        if food_id is not None:
            # print('one is ', food_id)
            context = fetch_all.food_item(food_id=food_id, rest_id=rest_id)
            return render(request, 'restApp/edit_particular_food.html', context)
        else:
            return redirect('/rest/edit_food')
    if request.method == 'POST':
        # print(request.POST)
        try:
            food_id = request.POST.get('food_id')
            name = request.POST.get('name')
            price = request.POST.get('price')
            offer = request.POST.get('offer')
            availibility = request.POST.get('availibility')
            description = request.POST.get('description')
            Type = request.POST.get('type')

            to_execute = "UPDATE FOOD_ITEM SET NAME={name},PRICE={price},OFFER={offer},AVAILIBILITY = {availibility}, DESCRIPTION={description},TYPE={type} " \
                         "WHERE ID = {id} and RESTAURANT_ID ={rest_id}"
            to_execute = to_execute.format(
                name=wrap_with_in_single_quote(name),
                price=price,
                offer=offer,
                availibility=wrap_with_in_single_quote(availibility),
                description=wrap_with_in_single_quote(description),
                type=wrap_with_in_single_quote(Type),
                id=wrap_with_in_single_quote(food_id),
                rest_id=wrap_with_in_single_quote(rest_id)
            )
            # print(to_execute)
            sql.execute(to_execute)

            rest = fetch_all.food_item(food_id, rest_id)
            context.update(rest)
            messages.info(request, "Successfully Updated")
            return render(request, "restApp/edit_particular_food.html", context)
        except Exception as e:
            print(e)
            messages.info(request, 'some error occured', )
            return redirect('/rest/edit_food')


def update_time(request):
    context = {}
    if not_this_season(request, app_name):
        messages.info(request, 'Please log in')
        return redirect('/rest')
    rest_id = request.session.get('id')
    context['hour_list'] = range(24)
    context['minute_list'] = range(0, 60, 1)
    if request.method == 'GET':
        rest = fetch_all.restaurant(rest_id)
        print(rest)
        context.update(rest)
        return render(request, 'restApp/update_time.html', context)
    elif request.method == 'POST':
        open_time = request.POST.get('openTime')
        close_time = request.POST.get('closeTime')
        cursor = sql.create_cursor()
        to_execute = "UPDATE RESTAURANT SET OPEN_TIME = {open_time}, CLOSE_TIME= {close_time} WHERE ID ={id}"
        to_execute = to_execute.format(
            open_time=wrap_with_in_single_quote(open_time),
            close_time=wrap_with_in_single_quote(close_time),
            id=wrap_with_in_single_quote(rest_id)
        )
        sql.execute(to_execute)
        rest = fetch_all.restaurant(rest_id)
        # print(rest)
        context.update(rest)
        messages.info(request, 'Update Done !!!')
        return render(request, 'restApp/update_time.html', context)


def update_logo(request):
    context = {}
    if not_this_season(request, app_name):
        messages.info(request, 'Please log in')
        return redirect('/rest')
    rest_id = request.session.get('id')
    if request.method == 'GET':
        rest = fetch_all.restaurant(rest_id)
        context.update(rest)
        return render(request, 'restApp/update_logo.html', context)
    elif request.method == 'POST':
        try:
            logo = request.FILES.get('restaurantLogo')
            if logo is not None:
                logo_path = 'rest' + rest_id + '.' + 'jpg'
                handle_uploaded_file(logo, logo_path, IMAGE_PATH + '/img/')
                handle_uploaded_file(logo, logo_path, STATIC_ROOT + '/img/')
            rest = fetch_all.restaurant(rest_id)
            # print(rest)
            context.update(rest)
            messages.info(request, 'Succcessfully updated LOGO !!!')
        except:
            messages.info(request, 'some error occured')
        finally:
            return render(request, 'restApp/update_logo.html', context)


def update_location(request):
    context = {}
    if not_this_season(request, app_name):
        messages.info(request, "Please Log in")
        return redirect('/rest')

    rest_id = request.session.get('id')
    if request.method == 'POST':
        location = request.POST.get('location')
        if location != request.session.get('location'):
            try:
                request.session['location'] = location
                to_execute = "UPDATE RESTAURANT SET LOCATION = {location} WHERE ID = {id}"
                to_execute = to_execute.format(
                    location=wrap_with_in_single_quote(location),
                    id=wrap_with_in_single_quote(rest_id)
                )
                print(to_execute)
                sql.execute(to_execute)
                messages.info(request, "Successfully updated location to " + location)
            except Exception as e:
                print(e)
                pass
    context['location'] = request.session.get('location')
    context['user_name'] = request.session.get('user_name')
    return render(request, 'restApp/update_location.html', context)
