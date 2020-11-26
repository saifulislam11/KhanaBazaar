from django.contrib import messages
from django.shortcuts import render

from helper import sql, fetch_all
from helper.read_write_to_file import handle_uploaded_file
from helper.wrap_and_encode import get_hashed_value, wrap_with_in_single_quote
# Create your views here.
from khanabazaar.settings import STATIC_ROOT, IMAGE_PATH


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
        rest = c.fetchone()
        c.close()
        if rest is None:
            messages.info(request, 'Please provide correct information')
            return render(request, 'restApp/sign_in.html', context)
        else:
            id = rest[0]
            name = rest[1]
            email = rest[7]
            # password = rest[8]
            request.session['id'] = id
            request.session['user_name'] = name
            request.session['email'] = email
            context['user_name'] = request.session.get('user_name')
            return render(request, 'restApp/index.html', context)

    elif request.method == 'GET':
        action = request.GET.get('action')
        if action == 'logout':
            request.session.flush()
            print('log out ing')
            return render(request, 'restApp/sign_in.html', context)

        if not request.session.is_empty():
            return render(request, 'restApp/index.html', context)
        else:
            return render(request, 'restApp/sign_in.html', context)

    return render(request, 'restApp/sign_in.html', context)


def add_food(request):
    context = {}
    if request.method == 'POST':
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

        try:
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
            print(to_execute)
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
            conn.rollback()
        finally:
            conn.close()

    return render(request, 'restApp/add_food.html', context)


def edit_food(request):
    context = {}
    if request.method == 'GET':

        if not request.session.is_empty():
            rest_id = request.session.get('id')
            context['foods'] = fetch_all.food_item_all(rest_id)
            return render(request, 'restApp/edit_food.html', context)

    return render(request, 'restApp/edit_food.html', context)


def edit_particular_food(request):
    context = {}
    if request.session.is_empty():
        return render(request, 'restApp/sign_in.html', context)
    rest_id = request.session.get('id')
    if request.method == 'GET':
        food_id = request.GET.get('rest')
        if food_id is not None:
            # print('one is ', food_id)
            context = fetch_all.food_item(food_id=food_id, rest_id=rest_id)

            return render(request, 'restApp/edit_particular_food.html', context)
    if request.method == 'POST':
        food_id = request.POST.get('id')
        name = request.POST.get('name')
        price = request.POST.get('price')
        offer = request.POST.get('offer')
        description = request.POST.get('description')
        Type = request.POST.get('type')

        to_execute = "UPDATE FOOD_ITEM SET NAME={name},PRICE={price},OFFER={offer},DESCRIPTION={description},TYPE={type} " \
                     "WHERE ID = {id} and RESTAURANT_ID ={rest_id}"
        to_execute = to_execute.format(
            name=wrap_with_in_single_quote(name),
            price=price,
            offer=offer,
            description=wrap_with_in_single_quote(description),
            type=wrap_with_in_single_quote(Type),
            id=wrap_with_in_single_quote(food_id),
            rest_id=wrap_with_in_single_quote(rest_id)
        )
        sql.execute(to_execute)
        #print(to_execute)
        rest = fetch_all.food_item(food_id, rest_id)
        context.update(rest)
        messages.info(request, "Successfully Updated")
        return render(request, "restApp/edit_particular_food.html", context)


def update_time(request):
    context = {}
    if request.session.is_empty():
        return render(request, 'restApp/sign_in.html', context)
    rest_id = request.session.get('id')
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
    if request.session.is_empty():
        return render(request, 'restApp/sign_in.html', context)
    rest_id = request.session.get('id')
    if request.method == 'GET':
        rest = fetch_all.restaurant(rest_id)
        context.update(rest)
        return render(request, 'restApp/update_logo.html', context)
    elif request.method == 'POST':
        logo = request.FILES.get('restaurantLogo')
        if logo is not None:
            logo_path = 'rest' + rest_id + '.' + 'jpg'
            handle_uploaded_file(logo, logo_path, IMAGE_PATH + '/img/')
            handle_uploaded_file(logo, logo_path, STATIC_ROOT + '/img/')
        rest = fetch_all.restaurant(rest_id)
        print(rest)
        context.update(rest)
        messages.info(request, 'Succcessfully updated LOGO !!!')
        return render(request, 'restApp/update_logo.html', context)
