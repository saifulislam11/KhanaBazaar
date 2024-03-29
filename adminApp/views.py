from shutil import copyfile

from django.contrib import messages
from django.shortcuts import render, redirect

from adminApp.urls import app_name
from helper import sql, fetch_all
from helper.promo import promo_exists
from helper.read_write_to_file import handle_uploaded_file
from helper.session import not_this_season
from helper.sql import get_next_id
from helper.wrap_and_encode import wrap_with_in_single_quote, get_hashed_value
from khanabazaar.settings import IMAGE_PATH, STATIC_ROOT, DEFAULT_IMAGE_PATH


# app_name = 'homeApp'

# Create your views here.

def index(request):
    context = {}
    not_this_season(request, app_name)
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            password = get_hashed_value(password)
            c = sql.create_cursor()
            to_execute = "Select * From ADMIN Where EMAIL = {email} " \
                         "and PASSWORD_HASH = {password}"
            to_execute = to_execute.format(
                email=wrap_with_in_single_quote(email),
                password=wrap_with_in_single_quote(password)
            )
            c.execute(to_execute)
            admin = c.fetchone()

            if admin is None:
                messages.info(request, "Incorrect credentials")
                return render(request, 'adminApp/sign_in.html', context)
            else:
                id = admin[0]
                last_name = admin[1]
                first_name = admin[2]
                request.session['id'] = id
                request.session['last_name'] = last_name
                request.session['first_name'] = first_name
                request.session['email'] = email
                request.session['app_name'] = app_name
                request.session['user_name'] = last_name
                context['user_name'] = last_name
                return render(request, 'adminApp/index.html', context)
        except Exception as e:
            print(e)
            messages.info(request, "Some unknown error occured!")
            return render(request, 'adminApp/index.html', context)
        finally:
            c.close()
            pass

    elif request.method == 'GET':
        try:
            action = request.GET.get('action')
            if action == 'logout':
                if not request.session.is_empty():
                    request.session.flush()
                    messages.info(request, 'You have successfully Log out!')
                    return render(request, 'adminApp/sign_in.html', context)

            if not request.session.is_empty():
                context['user_name'] = request.session.get('last_name')
                return render(request, 'adminApp/index.html', context)
            else:
                return render(request, 'adminApp/sign_in.html', context)
        except Exception as e:
            print(e)
            messages.info(request, "Some unknown error occured!")
            return render(request, 'adminApp/sign_in.html', context)


def add_restaurant(request):
    context = {}

    if not_this_season(request, app_name):
        messages.info(request, 'YOU ARE NOT LOGGED IN ')
        return redirect('/admin')
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            location = request.POST.get('location')
            logo = request.FILES.get('restaurantLogo')
            email = request.POST.get('email')
            open_time = request.POST.get('openTime')
            close_time = request.POST.get('closeTime')
            password1 = request.POST.get('password1')
            password1 = get_hashed_value(password1)
            password2 = request.POST.get('password2')
            id = get_next_id()
            logo_path = 'rest' + id + '.' + 'jpg'
            # print(type(logo))
            # print(logo)
            if logo is not None:
                handle_uploaded_file(logo, logo_path, IMAGE_PATH + '/img/')
                handle_uploaded_file(logo, logo_path, STATIC_ROOT + '/img/')
                # collectstatic()
            else:
                try:  # we will use rest0 as a default restaurant pic
                    image_path = DEFAULT_IMAGE_PATH + 'rest0.jpg'
                    copyfile(image_path, IMAGE_PATH + '/img/' + logo_path)
                    copyfile(image_path, STATIC_ROOT + '/img/' + logo_path)
                except Exception as e:
                    print(e)
                    pass
                finally:
                    pass

            to_execute = "INSERT INTO RESTAURANT(ID,NAME,LOCATION,LOGO_PATH,RATING,OPEN_TIME,CLOSE_TIME,EMAIL,PASSWORD_HASH)" \
                         "VALUES({id}, {name}, {location}, {logo_path}, {rating}, {open_time}, {close_time}, {email}, " \
                         "{password_hash}) "
            to_execute = to_execute.format(
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
            # print(wrap_with_in_single_quote(email))
            # print(to_execute)
            sql.execute(to_execute)

            # Now adding into relation manages
            to_execute = "INSERT INTO MANAGES(RESTAURANT_ID, ADMIN_ID) " \
                         "VALUES({restaurant_ID}, {admin_ID})"
            to_execute = to_execute.format(
                restaurant_ID=wrap_with_in_single_quote(id),
                admin_ID=wrap_with_in_single_quote(request.session.get('id')))
            # print(to_execute)
            sql.execute(to_execute)
            messages.info(request, 'Restaurant has been successfully added')
            return redirect('/admin/add_restaurant')
        except Exception as e:
            print(e)
            messages.info(request, 'restaurant was not added')
            return redirect('/admin/add_restaurant')
        finally:
            pass
    context.update(request.session)
    return render(request, 'adminApp/add_restaurant.html', context)


def add_food_man(request):
    """
    handles the view of add foodman
    :param request:
    :return:
    """
    context = {}
    if not_this_season(request, app_name):
        messages.info(request, 'Please sign in first')
        return redirect('/admin')
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            phone1 = request.POST.get('phone1')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password1 = get_hashed_value(password1)
            password2 = request.POST.get('password2')
            password2 = get_hashed_value(password2)
            vehicle_type = request.POST.get('vehicle_type')
            reg_no = request.POST.get('reg_no')
            salary = request.POST.get('salary')
            duration = request.POST.get('duration')  # in months
            init_rating = request.POST.get('init_rating')
            if init_rating is None:
                init_rating = 4.00
            profile_img = request.FILES.get('profile_img')
            profile_img_path = None
            foodman_id = get_next_id()
            profile_img_path = 'foodman' + foodman_id + '.' + 'jpg'
            if profile_img is not None:
                handle_uploaded_file(profile_img, profile_img_path, IMAGE_PATH + '/img/')
                handle_uploaded_file(profile_img, profile_img_path, STATIC_ROOT + '/img/')
            else:
                try:
                    image_path = DEFAULT_IMAGE_PATH + 'foodman0.jpg'
                    copyfile(image_path, IMAGE_PATH + '/img/' + profile_img_path)
                    copyfile(image_path, STATIC_ROOT + '/img/' + profile_img_path)
                except:
                    pass

            cursor = sql.create_cursor()
            admin_id = request.session.get('id')
            cursor.callproc('ADD_FOODMAN', [admin_id, foodman_id, name, email, password1, phone1,
                                            init_rating, profile_img_path, reg_no, vehicle_type, salary, duration])
            messages.info(request, "adding of foodman was successfull")

        except Exception as e:
            print("Something is not right. And why rollback is not working.")
            print(e)
            messages.info(request, "adding of foodman was unsuccessfull")

        finally:
            try:
                cursor.close()
            except:
                pass
    context.update(request.session)
    return render(request, 'adminApp/add_foodman.html', context)


def create_promo(request):
    """
    handles the view off adding promo
    :param request:
    :return:
    """
    context = {}
    # for r in request.session.items():
    #     print(r)
    if not_this_season(request, app_name):
        messages.info(request, "Something went wrong. Please Log in again")
        return redirect('/admin')
    if request.method == 'POST':
        name = request.POST.get('name')
        if promo_exists(name):
            messages.info(request, 'The promo exists')
        else:
            try:
                percent = request.POST.get('percent')
                fixed_amount = request.POST.get('fixed_amount')
                promo_limit = request.POST.get('promo_limit')
                min_order_value = request.POST.get('min_order_value')
                max_discount_amount = request.POST.get('max_discount_amount')
                promo_id = sql.get_next_id()
                to_execute = "INSERT INTO PROMO(ID, NAME, PERCENT, FIXED_AMOUNT, PROMO_LIMIT, MIN_ORDER_VALUE, " \
                             "MAX_DISCOUNT_AMOUNT)" \
                             "VALUES({id}, {name}, {percent}, {fixed_amount}, {promo_limit}, {min_order_value}, " \
                             "{max_discount_amount}) "
                to_execute = to_execute.format(
                    id=wrap_with_in_single_quote(promo_id),
                    name=wrap_with_in_single_quote(name),
                    percent=percent,
                    fixed_amount=fixed_amount,
                    promo_limit=promo_limit,
                    min_order_value=min_order_value,
                    max_discount_amount=max_discount_amount
                )
                # print(to_execute)
                sql.execute(to_execute)
                messages.info(request, 'Creation of promo is successful')
                # return redirect('/admin/create_promo', context)
            except Exception as e:
                messages.info(request, 'Promo was not created')
            finally:
                pass
    context.update(request.session)
    return render(request, 'adminApp/create_promo.html', context)


def edit_restaurant(request):
    context = {}

    return render(request, 'adminApp/edit_restaurant.html', context)


def offer_promo(request):
    context = {}
    if not_this_season(request, app_name):
        messages.info(request, "Something went wrong. Please Log in again")
        return redirect('/admin')
    if request.method == 'POST':
        customers = request.POST.get('customers')
        customers = customers.split(',')  # data was send via comma separated strings
        promo_id = request.POST.get('promo')
        if promo_id == '':
            messages.info(request, 'please select a promo')
        elif len(customers) == 0:
            messages.info(request, 'You have not selected any customer')
        else:
            try:
                cursor = sql.create_cursor()
                remaining_promo = fetch_all.promo(promo_id)['promo_limit']
                admin_id = request.session.get('id')
                print(admin_id)
                for customer_id in customers:
                    to_execute = "INSERT INTO OFFERS(ADMIN_ID, CUSTOMER_ID, PROMO_ID, REMAINING_PROMO) VALUES ({admin_id}, {customer_id}, {promo_id},{remaining_promo})"
                    to_execute = to_execute.format(
                        admin_id=wrap_with_in_single_quote(admin_id),
                        customer_id=wrap_with_in_single_quote(customer_id),
                        promo_id=wrap_with_in_single_quote(promo_id),
                        remaining_promo=remaining_promo
                    )
                    try:
                        sql.execute(to_execute)
                    except Exception as e:
                        print(e)
                        # print('the customer already has this promo')
                        pass
                    messages.info(request, 'Successfully distributed Promos')
            except Exception as e:
                # print('Error happen in writing in offer table ')
                print(e)
                messages.info(request, 'Some error occured! please Try again!')
                pass
    context.update(request.session)
    context['customers'] = fetch_all.customer_all()
    context['promos'] = fetch_all.promo_all()

    return render(request, 'adminApp/offer_promo.html', context)


def suspend_customer(request):
    context = {}
    if not_this_season(request, app_name):
        messages.info(request, "Something went wrong. Please Log in again")
        return redirect('/admin')
    if request.method == 'POST':
        try:

            customers = request.POST.get('customers')
            customers = customers.split(',')
            print(customers)
            cursor = sql.create_cursor()
            for customer_id in customers:
                cursor.callproc('SUSPEND_CUSTOMER', [customer_id])
            messages.info(request, 'Succesfully deleted all customer')
        except Exception as e:
            print(e)
            messages.info(request, 'Some error occured')
        finally:
            try:
                cursor.close()
            except:
                pass
    context.update(request.session)
    context['customers'] = fetch_all.customer_all()
    return render(request, 'adminApp/suspend_customer.html', context)


def suspend_foodman(request):
    context = {}
    if not_this_season(request, app_name):
        messages.info(request, "Something went wrong. Please Log in again")
        return redirect('/admin')
    if request.method == 'POST':
        try:
            foodmans = request.POST.get('foodmans')
            foodmans = foodmans.split(',')
            cursor = sql.create_cursor()
            for foodman_id in foodmans:
                cursor.callproc('SUSPEND_FOODMAN', [foodman_id])
            messages.info(request, 'Successfully deleted foodmans')
        except:
            messages.info(request, 'Some error occured')
            pass
        finally:
            try:
                cursor.close()
            except:
                pass
    context.update(request.session)
    context['foodmans'] = fetch_all.foodman_all()
    return render(request, 'adminApp/suspend_foodman.html', context)


if __name__ == '__main__':
    # havershine js plus leaflet js
    print(app_name)
    pass

# commented code segments

# add to foodman table
# to_execute = "INSERT INTO FOODMAN(ID, NAME, EMAIL, PASSWORD_HASH, RATING, IMAGE_PATH) " \
#              " VALUES({id}, {name}, {email},{password}, {rating},{profile_img_path})"
# to_execute = to_execute.format(
#     id=wrap_with_in_single_quote(foodman_id),
#     name=wrap_with_in_single_quote(name),
#     email=wrap_with_in_single_quote(email),
#     password=wrap_with_in_single_quote(password1),
#     rating=wrap_with_in_single_quote(init_rating),
#     profile_img_path=wrap_with_in_single_quote(profile_img_path)
# )
# print(to_execute)
# cursor.execute(to_execute)
# # add phone no
# to_execute = "INSERT INTO FOODMAN_PHONE(ID,PHONE_NO) " \
#              " VALUES({foodman_id},{phone})"
# to_execute = to_execute.format(
#     foodman_id=wrap_with_in_single_quote(foodman_id),
#     phone=wrap_with_in_single_quote(phone1)
# )
# print(to_execute)
# cursor.execute(to_execute)
#
# # Insert into vehicle table
# to_execute = "INSERT INTO VEHICLE(ID, REG_NO, TYPE) " \
#              " VALUES({vehicle_id}, {reg_no}, {type})"
# to_execute = to_execute.format(
#     vehicle_id=wrap_with_in_single_quote(vehicle_id),
#     reg_no=wrap_with_in_single_quote(reg_no),
#     type=wrap_with_in_single_quote(vehicle_type)
# )
# print(to_execute)
# cursor.execute(to_execute)
# # Insert into DELIVERS_BY table
# to_execute = "INSERT INTO DELIVERS_BY(FOODMAN_ID, VEHICLE_ID) " \
#              " VALUES({foodman_id}, {vehicle_id})"
# to_execute = to_execute.format(
#     foodman_id=wrap_with_in_single_quote(foodman_id),
#     vehicle_id=wrap_with_in_single_quote(vehicle_id)
# )
# print(to_execute)
# cursor.execute(to_execute)
# # Insert into CONTRACT table
# to_execute = "INSERT INTO CONTRACT(ID,DURATION, SALARY, INIT_RATING, DATE_OF_CONTRACT) " \
#              " VALUES({contract_id},{duration}, {salary},{init_rating}, SYSDATE)"
# to_execute = to_execute.format(
#     contract_id=wrap_with_in_single_quote(contract_id),
#     duration=wrap_with_in_single_quote(duration),
#     salary=wrap_with_in_single_quote(salary),
#     init_rating=init_rating
# )
# cursor.execute(to_execute)
#
# # Insert into APPOINTS table
# to_execute = "INSERT INTO APPOINTS(FOODMAN_ID, ADMIN_ID, CONTRACT_ID) " \
#              " VALUES({foodman_id}, {admin_id}, {contract_id})"
# to_execute = to_execute.format(
#     foodman_id=wrap_with_in_single_quote(foodman_id),
#     admin_id=wrap_with_in_single_quote(request.session.get('id')),
#     contract_id=wrap_with_in_single_quote(contract_id)
# )
# print(to_execute)
# cursor.execute(to_execute)
