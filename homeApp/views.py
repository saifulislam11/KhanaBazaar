from datetime import datetime, timedelta

import cx_Oracle
from django.shortcuts import render, redirect
import helper.wrap_and_encode

from helper import sql
from helper.sql import get_next_id
from helper.wrap_and_encode import wrap_with_in_single_quote, get_hashed_value
from homeApp.urls import app_name
from helper.session import not_this_season

con = cx_Oracle.connect("KB", "123", "localhost/orcl")
print("Connected!")
c = con.cursor()


# Create your views here.
def index(request):
    c = con.cursor()
    c.execute('select * from RESTAURANT')
    dict_result = []
    for row in c:
        id = row[0]
        name = row[1]
        path = row[3]
        dic = {'id': id, 'name': name, 'path': path}
        dict_result.append(dic)
    list1 = []
    list2 = []
    list3 = []
    brk = int(len(dict_result) / 3)
    for i in range(len(dict_result)):
        if (int(i / brk) == 0):
            list1.append(dict_result[i])
        elif (int(i / brk) == 1):
            list2.append(dict_result[i])
        else:
            list3.append(dict_result[i])
    
    #------------checking this session-----------#
    if not_this_season(request, app_name):
        c.close()
        return render(request, 'homeApp/index.html', {'list1': list1, 'list2': list2, 'list3': list3, 'contex': 'None'})


    # -------------logout--------------#
    if request.method == 'GET':
        print('get method')
        if 'action' in request.GET:
            action = request.GET.get('action')
            if action == 'logout':
                print('action logout')
                if request.session.has_key('first_name'):
                    print('has key in session')
                    request.session.flush()
                    return render(request, 'homeApp/index.html',
                                  {'list1': list1, 'list2': list2, 'list3': list3, 'contex': 'None'})
    if not request.session.is_empty() and request.session['app_name'] ==app_name:
        print('has session while in index')
        if 'first_name' in request.session:
            first_name = request.session['first_name']
        if 'id' in request.session:
            cust_id = request.session['id']
        command = "select * from CHOOSES WHERE CUSTOMER_ID = %s" % cust_id
        c.execute(command)
        orders = c.fetchall()
        
        order_dic=[]
        pay_id = None
        restaurant_dic = []
        for r in orders:
            order_id = r[0]
            table_name = '"' + "ORDER" + '"'
            command = "select * from {table_name} WHERE ID = %s" % order_id
            command = command.format(table_name="{}".format(table_name))
            c.execute(command)
            order = c.fetchall()
            temp_dic = None
            #-----------pay id-----------#
            command = "select * from PAYS WHERE ORDER_ID = %s" % order_id
            c.execute(command)
            pays = c.fetchall()
            
            for row in order:
                ord_id = row[0]
                ord_time = row[1]
                ord_deltime = row[2]
                ord_loc = row[3]
                temp_dic = {'order_id':ord_id,'order_time':ord_time,'delivery_time':ord_deltime,'delivery_location':ord_loc}
            for row in pays:
                pay_id = row[1]
                pay_data = {'pay_id':pay_id}
                temp_dic.update(pay_data)
                break
            command = "select * from SELECTED WHERE ORDER_ID = %s" % order_id
            c.execute(command)
            food_item = c.fetchall()
            for row in food_item:
                food_id = row[1]
                command = "select * from FOOD_ITEM WHERE ID = %s" % food_id
                c.execute(command)
                fooditem_tbl = c.fetchall()
                for fooditem in fooditem_tbl:
                    rest_id = fooditem[1]
                    command = "select * from RESTAURANT WHERE ID = %s" % rest_id
                    c.execute(command)
                    restaurant_tbl = c.fetchall()
                    for rest in restaurant_tbl:
                        restaurant_data = {'restaurant_id':rest[0],'restaurant_name':rest[1],'restaurant_location':rest[2],'restaurant_path':rest[3]}
                        temp_dic.update(restaurant_data)
                        order_dic.append(temp_dic)
                        break
                    break
                break


                   
        print(order_dic)
        print(restaurant_dic)

        c.close()
        return render(request, 'homeApp/homepage.html',
                      {'list1': list1, 'list2': list2, 'list3': list3, 'customer_name': first_name,'orders':order_dic})

    # connection.commit()
    # cursor.close()
    c.close()
    return render(request, 'homeApp/index.html', {'list1': list1, 'list2': list2, 'list3': list3, 'contex': 'None'})


# --------------------------after sign in --------------------------#
def homepage(request):
    c = con.cursor()
    c.execute('select * from RESTAURANT')
    dict_result = []
    for row in c:
        id = row[0]
        name = row[1]
        path = row[3]
        dic = {'id': id, 'name': name, 'path': path}
        dict_result.append(dic)
    list1 = []
    list2 = []
    list3 = []
    brk = int(len(dict_result) / 3)
    for i in range(len(dict_result)):
        if (int(i / brk) == 0):
            list1.append(dict_result[i])
        elif (int(i / brk) == 1):
            list2.append(dict_result[i])
        else:
            list3.append(dict_result[i])

    # connection.commit()
    # cursor.close()
    #-----------check session---------#
    if not_this_season(request, app_name):
        if request.method == 'POST':
            # ------------------sign up-------------#
            star = request.POST.get('star')
            print(star)
            print('hello world')
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email_log = request.POST.get('email')
            phone = request.POST.get('phone')
            password1 = request.POST.get('password')
            password1 = get_hashed_value(password1)
            password2 = request.POST.get('confirmpassword')
            address = request.POST.get('address')
            id = get_next_id()
            # print(firstname+lastname+address)
            if (firstname != None and lastname != None and email_log != None):
                to_execute = "INSERT INTO CUSTOMER(ID,LAST_NAME,FIRST_NAME,EMAIL,PASSWORD_HASH,ADDRESS)" \
                            " VALUES({id}, {lastname}, {firstname}, {email}, {password_hash}, {address}) "
                to_execute_phone = "INSERT INTO CUSTOMER_PHONE(CUSTOMER_ID,PHONE_NO)" \
                                " VALUES({id}, {phone}) "
                to_execute_phone = to_execute_phone.format(
                    id=wrap_with_in_single_quote(id),
                    phone=wrap_with_in_single_quote(phone)
                )
                to_execute = to_execute.format(
                    id=wrap_with_in_single_quote(id),
                    firstname=wrap_with_in_single_quote(firstname),
                    lastname=wrap_with_in_single_quote(lastname),
                    email=wrap_with_in_single_quote(email_log),
                    password_hash=wrap_with_in_single_quote(password1),
                    address=wrap_with_in_single_quote(address)
                )

                info = id + ' ' + firstname + ' ' + lastname + ' ' + email_log
                customer_info = info.split(' ')
                print(customer_info)

                # print(firstname+lastname+address)
                print(to_execute)
                try:
                    sql.execute(to_execute)
                    sql.execute(to_execute_phone)
                    contex = 'registered successfully'
                    return render(request, 'homeApp/index.html',
                                {'list1': list1, 'list2': list2, 'list3': list3, 'contex': contex})

                except:
                    print("Something is not right. And why rollback is not working.")
                    sql.rollback()
                    # messages.info(request, "adding of foodman was unsuccessfull")
                    return render(request, 'homeApp/index.html', {'list1': list1, 'list2': list2, 'list3': list3,
                                                                'contex': 'something went wrong.try again'})

                finally:
                    c.close()
                    sql.commit()

                # return render(request, 'homeApp/homepage.html',{'list1':list1,'list2':list2,'list3':list3,'customer':customer_info,'customer_name':firstname})
            if lastname == None:
                # ---------------------sign up--------------------#
                c.close()
                connect = sql.create_cursor()
                email = request.POST['email']
                password = request.POST['password']
                password = get_hashed_value(password)
                print(email, password)
                to_execute = "Select * From CUSTOMER Where EMAIL = {email} " \
                            "and PASSWORD_HASH = {password}"
                to_execute = to_execute.format(
                    email=wrap_with_in_single_quote(email),
                    password=wrap_with_in_single_quote(password)
                )
                connect.execute(to_execute)
                customer = connect.fetchone()
                connect.close()
                customer = list(customer)
                print(customer)

                if customer is None:
                    print('no customer found')
                    return render(request, 'homeApp/index.html',
                                {'list1': list1, 'list2': list2, 'list3': list3, 'contex': 'None'})
                else:
                    cprime = con.cursor()
                    print('We need to do something')
                    id = customer[0]
                    last_name = customer[1]
                    first_name = customer[2]
                    request.session['id'] = id
                    request.session['last_name'] = last_name
                    request.session['first_name'] = first_name
                    request.session['email'] = email
                    request.session['app_name'] = app_name
                    # info = id + ' ' +firstname +' '+lastname+' '+email
                    # customer_info= info.split(' ')
                    cust_id = id
                    command = "select * from CHOOSES WHERE CUSTOMER_ID = %s" % cust_id
                    cprime.execute(command)
                    orders = cprime.fetchall()
                    
                    order_dic=[]
                    pay_id = None
                    restaurant_dic = []
                    for r in orders:
                        order_id = r[0]
                        table_name = '"' + "ORDER" + '"'
                        command = "select * from {table_name} WHERE ID = %s" % order_id
                        command = command.format(table_name="{}".format(table_name))
                        cprime.execute(command)
                        order = cprime.fetchall()
                        temp_dic = None
                        #-----------pay id-----------#
                        command = "select * from PAYS WHERE ORDER_ID = %s" % order_id
                        cprime.execute(command)
                        pays = cprime.fetchall()
                        for row in order:
                            ord_id = row[0]
                            ord_time = row[1]
                            ord_deltime = row[2]
                            ord_loc = row[3]
                            temp_dic = {'order_id':ord_id,'order_time':ord_time,'delivery_time':ord_deltime,'delivery_location':ord_loc}
                        for row in pays:
                            pay_id = row[1]
                            pay_data = {'pay_id':pay_id}
                            temp_dic.update(pay_data)
                            break
                        command = "select * from SELECTED WHERE ORDER_ID = %s" % order_id
                        cprime.execute(command)
                        food_item = cprime.fetchall()
                        for row in food_item:
                            food_id = row[1]
                            command = "select * from FOOD_ITEM WHERE ID = %s" % food_id
                            cprime.execute(command)
                            fooditem_tbl = cprime.fetchall()
                            for fooditem in fooditem_tbl:
                                rest_id = fooditem[1]
                                command = "select * from RESTAURANT WHERE ID = %s" % rest_id
                                cprime.execute(command)
                                restaurant_tbl = cprime.fetchall()
                                for rest in restaurant_tbl:
                                    restaurant_data = {'restaurant_id':rest[0],'restaurant_name':rest[1],'restaurant_location':rest[2],'restaurant_path':rest[3]}
                                    temp_dic.update(restaurant_data)
                                    order_dic.append(temp_dic)
                                    break
                                break
                            break


                            
                    print(order_dic)
                    print(restaurant_dic)
                    cprime.close()

                    return render(request, 'homeApp/homepage.html',
                                {'list1': list1, 'list2': list2, 'list3': list3, 'customer': customer,
                                'customer_name': customer[2],'orders':order_dic})
            else:
                return redirect('/homepage')
        else:
            print('couldnt fetch post method')
            return render(request, 'homeApp/index.html', {'list1': list1, 'list2': list2, 'list3': list3, 'contex': 'None'})
        c.close()

    # ----------------sign in----------------#
    if not request.session.is_empty() and request.session['app_name'] ==app_name:
        print('has session')
        if 'first_name' in request.session:
            first_name = request.session['first_name']
        if 'id' in request.session:
            cust_id = request.session['id']
        star = None
        if request.method == 'POST' and request.POST.get('feedback')!=None:
            feedback = request.POST.get('feedback')
            star = request.POST.get('star')
            image = request.POST.get('imagefile')
            pay_id = request.POST.get('pay_id')
            restaurant_id = request.POST.get('restaurant_id')


            print(star+' '+feedback+' '+image+' '+pay_id+' '+restaurant_id)
            review_id = get_next_id()
            now = datetime.now()
            review_time = now.strftime("%d/%m/%Y %H:%M:%S")
            comment = '"' + "COMMENT" + '"'
            

            command = "INSERT INTO REVIEW(ID,FOOD_RATING,{comment},DATE_TIME)" \
                " VALUES({review_id},{star},{feedback}, to_date({review_time},'DD/MM/YYYY HH24:MI:SS')) "
            command = command.format(
            comment = comment.format(comment="{}".format(comment)),
            review_id=wrap_with_in_single_quote(review_id),
            star=wrap_with_in_single_quote(star),
            feedback=wrap_with_in_single_quote(feedback),
            review_time=wrap_with_in_single_quote(review_time)
            )
            print(command)
            sql.execute(command)
            command = "INSERT INTO REVIEW_IMAGE(REVIEW_ID,IMAGE_PATH)" \
                " VALUES({review_id},{image}) "
            command = command.format(
            review_id=wrap_with_in_single_quote(review_id),
            image=wrap_with_in_single_quote(image)
            )
            sql.execute(command)
            command = "INSERT INTO REVIEWS(CUSTOMER_ID,PAY_ID,RESTAURANT_ID,REVIEW_ID)" \
                " VALUES({cust_id},{pay_id},{restaurant_id},{review_id}) "
            command = command.format(
            cust_id=wrap_with_in_single_quote(cust_id),
            pay_id=wrap_with_in_single_quote(pay_id),
            restaurant_id=wrap_with_in_single_quote(restaurant_id),
            review_id=wrap_with_in_single_quote(review_id)
            )
            sql.execute(command)



        command = "select * from CHOOSES WHERE CUSTOMER_ID = %s" % cust_id
        c.execute(command)
        orders = c.fetchall()
        
        order_dic=[]
        pay_id = None
        restaurant_dic = []
        for r in orders:
            order_id = r[0]
            table_name = '"' + "ORDER" + '"'
            command = "select * from {table_name} WHERE ID = %s" % order_id
            command = command.format(table_name="{}".format(table_name))
            c.execute(command)
            order = c.fetchall()
            #-----------pay id-----------#
            command = "select * from PAYS WHERE ORDER_ID = %s" % order_id
            c.execute(command)
            pays = c.fetchall()
            temp_dic = None
            for row in order:
                ord_id = row[0]
                ord_time = row[1]
                ord_deltime = row[2]
                ord_loc = row[3]
                temp_dic = {'order_id':ord_id,'order_time':ord_time,'delivery_time':ord_deltime,'delivery_location':ord_loc}
            for row in pays:
                pay_id = row[1]
                pay_data = {'pay_id':pay_id}
                temp_dic.update(pay_data)
                break
            command = "select * from SELECTED WHERE ORDER_ID = %s" % order_id
            c.execute(command)
            food_item = c.fetchall()
            for row in food_item:
                food_id = row[1]
                command = "select * from FOOD_ITEM WHERE ID = %s" % food_id
                c.execute(command)
                fooditem_tbl = c.fetchall()
                for fooditem in fooditem_tbl:
                    rest_id = fooditem[1]
                    command = "select * from RESTAURANT WHERE ID = %s" % rest_id
                    c.execute(command)
                    restaurant_tbl = c.fetchall()
                    for rest in restaurant_tbl:
                        restaurant_data = {'restaurant_id':rest[0],'restaurant_name':rest[1],'restaurant_location':rest[2],'restaurant_path':rest[3]}
                        temp_dic.update(restaurant_data)
                        order_dic.append(temp_dic)
                        break
                    break
                break


                   
        print(order_dic)
        print(restaurant_dic)
        
        return render(request, 'homeApp/homepage.html',
                      {'list1': list1, 'list2': list2, 'list3': list3, 'customer_name': first_name,'orders':order_dic})
    
    
    # ---------------------end of sign in ------------------#


# --------------------customer register-------------------#
'''def add_customer(request):
    context = {}

    if request.session.is_empty():
        messages.info(request, 'YOU ARE NOT LOGGED IN ')
        return redirect('/')
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password1 = get_hashed_value(password1)
        password2 = request.POST.get('confirmpassword')
        address = request.POST.get('address')
        id = get_next_id()
        print(firstname+lastname+address)
        to_execute = "INSERT INTO CUSTOMER(ID,LAST_NAME,FIRST_NAME,EMAIL,PASSWORD_HASH,ADDRESS)" \
                     "VALUES({id}, {lastname}, {firstname}, {email}, {password_hash}, {address} "
        to_execute = to_execute.format(
            id=wrap_with_in_single_quote(id),
            firstname=wrap_with_in_single_quote(firstname),
            lastname=wrap_with_in_single_quote(lastname),
            email=wrap_with_in_single_quote(email),
            password_hash=wrap_with_in_single_quote(password1),
            address=wrap_with_in_single_quote(address)
        )
        print(firstname+lastname+address)
        print(to_execute)
        c.execute(to_execute)

        # Now adding into relation manages
        to_execute = "INSERT INTO MANAGES(RESTAURANT_ID, ADMIN_ID) " \
                     "VALUES({restaurant_ID}, {admin_ID})"
        to_execute = to_execute.format(
            restaurant_ID=wrap_with_in_single_quote(id),
            admin_ID=wrap_with_in_single_quote(request.session.get('id')))
        # print(to_execute)
        sql.execute(to_execute)
        messages.info(request, 'Adding Done')
        return redirect('/homepage')
    return render(request, 'homeApp/index.html', context)'''


def aboutus(request):
    return render(request, 'homeApp/aboutus.html')


def contactus(request):
    return render(request, 'homeApp/contactus.html')


# payment method
def payment(request):
    c = con.cursor()
    price = request.POST.get('price')
    foods = request.POST.get('foods')
    prices = request.POST.get('prices')
    counts = request.POST.get('counts')
    restaurant = request.POST.get('restaurant')
    items = request.POST.get('items')
    food_collections = foods.split("#")
    count_collections = counts.split("#")
    price_collections = prices.split("#")
    ##removing last element
    all_food = []
    all_count = []
    all_price = []
    for i in range(len(food_collections) - 1):
        all_count.append(count_collections[i])
        all_food.append(food_collections[i])
        all_price.append(price_collections[i])

    print(restaurant)
    print(type(restaurant))
    print(all_food)
    print(all_count)
    print(all_price)
    print(price)
    print(items)
    sql = "select * from RESTAURANT WHERE ID= %s" % restaurant

    c.execute(sql)

    for row in c:
        id = row[0]
        name = row[1]
        path = row[3]
        rest_dic = {'id': id, 'name': name, 'path': path}

    print(rest_dic)
    cart_dic = []
    for i in range(len(all_food)):
        food = all_food[i]
        amount = all_price[i]
        count = all_count[i]
        dic = {'food': food, 'price': amount, 'count': count}
        cart_dic.append(dic)
    print(cart_dic)
    c.close()
    # info from session
    if 'first_name' in request.session:
        first_name = request.session['first_name']
    if 'id' in request.session:
        id = request.session['id']
    if 'last_name' in request.session:
        last_name = request.session['last_name']
    if 'email' in request.session:
        email = request.session['email']
    print(email + last_name)
    #---------for promo-----------#
    c = con.cursor()
    command = "Select * From OFFERS Where CUSTOMER_ID = %s" % id
    c.execute(command)
    promos = c.fetchall()
    print(promos)
    print('hello')
    promo =[]
    available_promo = []
    for row in promos:
        promo_id = row[2]
        remainings = row[3]
        command = "Select * From PROMO Where ID = %s" % promo_id
        c.execute(command)
        single_promo = c.fetchall()
        for row2 in single_promo:
            if int(price) >= int(row2[5]):
                dic = {'id':row2[0],'name':row2[1],'percent':row2[2],'fixed_amount':row2[3],'promo_limit':row2[4],'min_order_value':row2[5],'max_discount_value':row2[6],'remaining_promo':remainings}
                promo.append(dic)

    print(promo)
    c.close()

    

    return render(request, 'homeApp/payment.html',
                  {'price': price, 'items': len(cart_dic), 'restaurant': rest_dic, 'cart': cart_dic,
                   'customer_name': first_name, 'last_name': last_name, 'email': email,'foods':foods,'promos':promo})


def restaurant(request):
    c = con.cursor()
    c.execute('select * from RESTAURANT')
    query = None
    results = None
    email = None
    password = None
    if request.method == 'POST':
        query = request.POST.get('restaurant')
        email = request.POST['email']
        password = request.POST['password']
        print('chole')

        print(query)
        test = 0
        for row in c:
            # print(row[1])
            if len(query) == 0 or str(row[1].lower()).find(str(query.lower())) == -1:
                test = 0

            elif str(row[1].lower()).find(str(query.lower())) != -1:
                results = row[3]
                title = row[1]
                REST_id = row[0]
                test = 1
                id = row[0]
                break

                # print(row[3])
        print(test)
        if test == 0:
            c.close()
            return render(request, 'homeApp/restaurant.html', {'path': None})
        else:
            print(type(id))
            print(id)
            command = "select * from FOOD_ITEM WHERE RESTAURANT_ID = %s" % id
            c.execute(command)
            foods = c.fetchall()

            dict_result = []
            types = []
            for row in foods:
                id = row[0]
                id = str(id)
                command = "select * from FOOD_ITEM_PATH WHERE ID = %s" % id
                c.execute(command)
                food_path = c.fetchall()
                path = None
                for r in food_path:
                    path = r[1]
                name = row[2]
                price = row[3]
                food_type = row[7]
                print(id + ' ' + name + ' ' + food_type + ' ' + path)
                types.append(food_type)
                dic = {'id': id, 'name': name, 'price': price, 'type': food_type, 'path': path}
                dict_result.append(dic)
            types_set = set(types)
            unique_types = list(types_set)
            c.close()
            if not request.session.is_empty() and request.session['app_name'] ==app_name :
                print('has session')
                if 'first_name' in request.session:
                    first_name = request.session['first_name']
                if 'id' in request.session:
                    id = request.session['id']
                if 'last_name' in request.session:
                    last_name = request.session['last_name']
                if 'email' in request.session:
                    email = request.session['email']
                customer_dict = {'id': id, 'last_name': last_name, 'first_name': first_name, 'email': email}
                print(customer_dict)
                #---------for promo-----------#
                c = con.cursor()
                command = "Select * From OFFERS Where CUSTOMER_ID = %s" % id
                c.execute(command)
                promos = c.fetchall()
                print(promos)
                print('hello')
                promo =[]
                for row in promos:
                    promo_id = row[2]
                    command = "Select * From PROMO Where ID = %s" % promo_id
                    c.execute(command)
                    single_promo = c.fetchall()
                    for row2 in single_promo:
                        dic = {'id':row2[0],'name':row2[1],'percent':row2[2],'fixed_amount':row2[3],'promo_limit':row2[4],'min_order_value':row2[5],'max_discount_value':row2[6]}
                        promo.append(dic)
                print(promo)
                c.close()



                return render(request, 'homeApp/restaurant.html',
                              {'path': results, 'ID': REST_id, 'title': title, 'foods': dict_result,
                               'all_types': unique_types, 'customer_name': first_name, 'customer_dic': customer_dict,'promos':promo})
            elif email == "None" or password == "None":
                return render(request, 'homeApp/restaurant_log_in.html',
                              {'path': results, 'ID': REST_id, 'title': title, 'foods': dict_result,
                               'all_types': unique_types, 'customer_name': 'none'})
            else:
                print(email + ' ' + password)
                # c.close()
                connect = sql.create_cursor()
                password = get_hashed_value(password)
                print(email, password)
                to_execute = "Select * From CUSTOMER Where EMAIL = {email} " \
                             "and PASSWORD_HASH = {password}"
                to_execute = to_execute.format(
                    email=wrap_with_in_single_quote(email),
                    password=wrap_with_in_single_quote(password)
                )
                connect.execute(to_execute)
                customer = connect.fetchone()
                connect.close()
                '''customer = list(customer)
                print(customer)'''

                if customer is None:
                    print('no customer found')
                    return render(request, 'homeApp/restaurant_log_in.html',
                                  {'path': results, 'ID': REST_id, 'title': title, 'foods': dict_result,
                                   'all_types': unique_types, 'customer_name': 'none'})
                else:
                    print('We need to do something')
                    id = customer[0]
                    last_name = customer[1]
                    first_name = customer[2]
                    email = customer[3]
                    address = customer[5]
                    customer_dict = {'id': id, 'last_name': last_name, 'first_name': first_name, 'email': email,
                                     'address': address}
                    print(customer_dict)
                    request.session['id'] = id
                    request.session['last_name'] = last_name
                    request.session['first_name'] = first_name
                    request.session['email'] = email
                    request.session['app_name'] = app_name
                    # info = id + ' ' +firstname +' '+lastname+' '+email
                    # customer_info= info.split(' ')
                    #---------for promo-----------#
                    c = con.cursor()
                    command = "Select * From OFFERS Where CUSTOMER_ID = %s" % id
                    c.execute(command)
                    promos = c.fetchall()
                    print(promos)
                    print('hello')
                    promo =[]
                    for row in promos:
                        promo_id = row[2]
                        command = "Select * From PROMO Where ID = %s" % promo_id
                        c.execute(command)
                        single_promo = c.fetchall()
                        for row2 in single_promo:
                            dic = {'id':row2[0],'name':row2[1],'percent':row2[2],'fixed_amount':row2[3],'promo_limit':row2[4],'min_order_value':row2[5],'max_discount_value':row2[6]}
                            promo.append(dic)
                    print(promo)
                    c.close()

                    return render(request, 'homeApp/restaurant.html',
                                  {'path': results, 'ID': REST_id, 'title': title, 'foods': dict_result,
                                   'all_types': unique_types, 'customer_name': first_name,
                                   'customer_dic': customer_dict,'promos':promo})
                # return render(request,'homeApp/restaurant_log_in.html',{'path':results,'ID':REST_id,'title':title,'foods':dict_result,'all_types':unique_types,'customer_name':'none'})
                '''return render(request, 'homeApp/restaurant.html',
                                  {'path': results, 'ID': REST_id, 'title': title, 'foods': dict_result,
                                   'all_types': unique_types, 'customer_name': first_name})
                # return render(request,'homeApp/restaurant_log_in.html',{'path':results,'ID':REST_id,'title':title,'foods':dict_result,'all_types':unique_types,'customer_name':'none'})'''
    elif request.method == 'GET':
        print('get method')
        if 'action' in request.GET:
            action = request.GET.get('action')
            print(action)
            
            to_execute = "Select * From RESTAURANT Where NAME = {action} "
            to_execute = to_execute.format(
                    action=wrap_with_in_single_quote(action),
                )
            c.execute(to_execute)
            rest_tbl = c.fetchall()
            REST_id = None
            for r in rest_tbl:
                REST_id = r[0]
                title = r[1]
                results = r[3]
                print(REST_id)
            command = "select * from FOOD_ITEM WHERE RESTAURANT_ID = %s" % REST_id
            c.execute(command)
            foods = c.fetchall()

            dict_result = []
            types = []
            for row in foods:
                id = row[0]
                id = str(id)
                command = "select * from FOOD_ITEM_PATH WHERE ID = %s" % id
                c.execute(command)
                food_path = c.fetchall()
                path = None
                for r in food_path:
                    path = r[1]
                name = row[2]
                price = row[3]
                food_type = row[7]
                print(id + ' ' + name + ' ' + food_type + ' ' + path)
                types.append(food_type)
                dic = {'id': id, 'name': name, 'price': price, 'type': food_type, 'path': path}
                dict_result.append(dic)
            types_set = set(types)
            unique_types = list(types_set)
            c.close()
            #-----------checking session-----------#
            if not_this_season(request, app_name):
                return render(request, 'homeApp/restaurant_log_in.html',
                              {'path': results, 'ID': REST_id, 'title': title, 'foods': dict_result,
                               'all_types': unique_types, 'customer_name': 'none'})

            if not request.session.is_empty() and request.session['app_name'] ==app_name:
                print('has session')
                if 'first_name' in request.session:
                    first_name = request.session['first_name']
                if 'id' in request.session:
                    id = request.session['id']
                if 'last_name' in request.session:
                    last_name = request.session['last_name']
                if 'email' in request.session:
                    email = request.session['email']
                customer_dict = {'id': id, 'last_name': last_name, 'first_name': first_name, 'email': email}
                print(customer_dict)
                #---------for promo-----------#
                c = con.cursor()
                command = "Select * From OFFERS Where CUSTOMER_ID = %s" % id
                c.execute(command)
                promos = c.fetchall()
                print(promos)
                print('hello')
                promo =[]
                for row in promos:
                    promo_id = row[2]
                    command = "Select * From PROMO Where ID = %s" % promo_id
                    c.execute(command)
                    single_promo = c.fetchall()
                    for row2 in single_promo:
                        dic = {'id':row2[0],'name':row2[1],'percent':row2[2],'fixed_amount':row2[3],'promo_limit':row2[4],'min_order_value':row2[5],'max_discount_value':row2[6]}
                        promo.append(dic)
                print(promo)
                c.close()
                return render(request, 'homeApp/restaurant.html',
                              {'path': results, 'ID': REST_id, 'title': title, 'foods': dict_result,
                               'all_types': unique_types, 'customer_name': first_name, 'customer_dic': customer_dict,'promos':promo})
            elif email == None or password == None:
                return render(request, 'homeApp/restaurant_log_in.html',
                              {'path': results, 'ID': REST_id, 'title': title, 'foods': dict_result,
                               'all_types': unique_types, 'customer_name': 'none'})
            else:
                print(email + ' ' + password)
                # c.close()
                connect = sql.create_cursor()
                password = get_hashed_value(password)
                print(email, password)
                to_execute = "Select * From CUSTOMER Where EMAIL = {email} " \
                             "and PASSWORD_HASH = {password}"
                to_execute = to_execute.format(
                    email=wrap_with_in_single_quote(email),
                    password=wrap_with_in_single_quote(password)
                )
                connect.execute(to_execute)
                customer = connect.fetchone()
                connect.close()
                '''customer = list(customer)
                print(customer)'''

                if customer is None:
                    print('no customer found')
                    return render(request, 'homeApp/restaurant_log_in.html',
                                  {'path': results, 'ID': REST_id, 'title': title, 'foods': dict_result,
                                   'all_types': unique_types, 'customer_name': 'none'})
                else:
                    print('We need to do something')
                    id = customer[0]
                    last_name = customer[1]
                    first_name = customer[2]
                    email = customer[3]
                    address = customer[5]
                    customer_dict = {'id': id, 'last_name': last_name, 'first_name': first_name, 'email': email,
                                     'address': address}
                    print(customer_dict)
                    request.session['id'] = id
                    request.session['last_name'] = last_name
                    request.session['first_name'] = first_name
                    request.session['email'] = email
                    request.session['app_name'] = app_name
                    #---------for promo-----------#
                    c = con.cursor()
                    command = "Select * From OFFERS Where CUSTOMER_ID = %s" % id
                    c.execute(command)
                    promos = c.fetchall()
                    print(promos)
                    print('hello')
                    promo =[]
                    for row in promos:
                        promo_id = row[2]
                        command = "Select * From PROMO Where ID = %s" % promo_id
                        c.execute(command)
                        single_promo = c.fetchall()
                        for row2 in single_promo:
                            dic = {'id':row2[0],'name':row2[1],'percent':row2[2],'fixed_amount':row2[3],'promo_limit':row2[4],'min_order_value':row2[5],'max_discount_value':row2[6]}
                            promo.append(dic)
                    print(promo)
                    c.close()
                    # info = id + ' ' +firstname +' '+lastname+' '+email
                    # customer_info= info.split(' ')

                    return render(request, 'homeApp/restaurant.html',
                                  {'path': results, 'ID': REST_id, 'title': title, 'foods': dict_result,
                                   'all_types': unique_types, 'customer_name': first_name,
                                   'customer_dic': customer_dict,'promos':promo})
            #return render(request, 'homeApp/restaurant.html')


def confirm_payment(request):
    c = con.cursor()
    if 'first_name' in request.session:
        first_name = request.session['first_name']
    if 'id' in request.session:
        cust_id = request.session['id']
    if 'last_name' in request.session:
        last_name = request.session['last_name']
    if 'email' in request.session:
        email = request.session['email']
    if request.method == 'POST':
        order_price = request.POST.get('order_price')
        delivery_type = request.POST.get('delivery_type')
        delivery_location = request.POST.get('delivery_address')
        foods = request.POST.get('ordered_foods')
        restaurant_id = request.POST.get('restaurant_name')
        promo = request.POST.get('promo_used')
        order_id = get_next_id()
        print(order_price + ' ' + delivery_location + ' ' + delivery_type+' '+foods)
        #-------------getting foods-----------#
        food_collections = foods.split("#")
        all_food = []
        for i in range(len(food_collections) - 1):
            all_food.append(food_collections[i])
        #---------end of foods------------#
        

        #----------getting current date--------#
        now = datetime.now()
        order_time = now.strftime("%d/%m/%Y %H:%M:%S")
        print(order_time)
        delivery_time = helper.wrap_and_encode.not_picked_date
        delivery_time = delivery_time.strftime("%d/%m/%Y %H:%M:%S")
        print(delivery_time)
        #---------------end of getting current date-----------#

        #-------------promo uses-------------#
        print(promo)
        if promo != "Not now":
            print(promo)
            to_execute = "SELECT * FROM PROMO WHERE NAME ={promo}"
            to_execute = to_execute.format(
                    promo=wrap_with_in_single_quote(promo)
                )
            c.execute(to_execute)
            promo_tbl = c.fetchall()
            for r in promo_tbl:
                promo_id = r[0]
                to_execute_uses = "INSERT INTO USES(ORDER_ID,PROMO_ID) VALUES({order_id},{promo_id})"
                to_execute_uses = to_execute_uses.format(
                    order_id=wrap_with_in_single_quote(order_id),
                    promo_id=wrap_with_in_single_quote(promo_id)
                )
                print(to_execute)
                #---------update promo remainings
                to_execute_offers = "SELECT * FROM OFFERS WHERE PROMO_ID ={promo_id}"
                to_execute_offers = to_execute_offers.format(
                        promo_id=wrap_with_in_single_quote(promo_id)
                    )
                c.execute(to_execute_offers)
                offers_tbl = c.fetchall()
                for r in offers_tbl:
                    remaining_promo = int(r[3])
                    remaining_promo = int(remaining_promo) -1
                    if remaining_promo<=0:
                        remaining_promo = 0

                    to_execute_update = "UPDATE OFFERS SET REMAINING_PROMO = {remaining_promo} WHERE PROMO_ID = {promo_id}"
                    to_execute_update = to_execute_update.format(
                    remaining_promo=wrap_with_in_single_quote(remaining_promo),
                    promo_id=wrap_with_in_single_quote(promo_id)
                    )
                    print(to_execute_update)
            
        #----------------end of promo----------------#

            
            

        
        table_name = '"' + "ORDER" + '"'
        print(table_name)
        to_execute = "INSERT INTO {table_name}(ID,ORDER_TIME,DELIVERY_TIME,DELIVERY_LOCATION)" \
                     " VALUES({order_id}, to_date({order_time},'DD/MM/YYYY HH24:MI:SS'), to_date({delivery_time},'DD/MM/YYYY HH24:MI:SS'), {delivery_location}) "
        to_execute = to_execute.format(
            table_name="{}".format(table_name),
            order_id=wrap_with_in_single_quote(order_id),
            order_time=wrap_with_in_single_quote(order_time),
            delivery_time=wrap_with_in_single_quote(delivery_time),
            delivery_location=wrap_with_in_single_quote(delivery_location)
        )
        payment_id = get_next_id()
        to_execute_payment = "INSERT INTO PAYMENT(ID,PAYING_AMOUNT,PAYMENT_TYPE,DATE_TIME)" \
                     " VALUES({payment_id},{order_price},{delivery_type}, to_date({order_time},'DD/MM/YYYY HH24:MI:SS')) "
        to_execute_payment = to_execute_payment.format(
            payment_id=wrap_with_in_single_quote(payment_id),
            order_price=wrap_with_in_single_quote(order_price),
            delivery_type=wrap_with_in_single_quote(delivery_type),
            order_time=wrap_with_in_single_quote(order_time)
        )
        to_execute_chooses = "INSERT INTO CHOOSES(ORDER_ID,CUSTOMER_ID)" \
                     " VALUES({order_id},{cust_id}) "
        to_execute_chooses = to_execute_chooses.format(
            order_id=wrap_with_in_single_quote(order_id),
            cust_id = wrap_with_in_single_quote(cust_id)
        )
        to_execute_pays = "INSERT INTO PAYS(ORDER_ID,PAY_ID)" \
                     " VALUES({order_id},{payment_id}) "
        to_execute_pays = to_execute_pays.format(
            order_id=wrap_with_in_single_quote(order_id),
            payment_id = wrap_with_in_single_quote(payment_id)
        )

        info = order_id + ' ' + delivery_time + ' ' + order_time + ' ' + delivery_location
        order_info = info.split(' ')
        print(order_info)

        # print(firstname+lastname+address)
        print(to_execute)
        try:
            sql.execute(to_execute)
            sql.execute(to_execute_chooses)
            sql.execute(to_execute_payment)
            sql.execute(to_execute_pays)
            if promo != "Not now":
                print('still now ok')
                sql.execute(to_execute_uses)
                print('still now ok')
                sql.execute(to_execute_update)
            contex = 'ordered successfully'

        except:
            print("Something is not right. And why rollback is not working.")
            sql.rollback()
            # messages.info(request, "adding of foodman was unsuccessfull")

        finally:
            sql.commit()

        #------------------selected-------------#
        for i in range(len(all_food)):
            food = all_food[i]
            to_execute = "Select * From FOOD_ITEM Where NAME = {food} " \
                             "and RESTAURANT_ID = {restaurant_id}"
            to_execute = to_execute.format(
                    food=wrap_with_in_single_quote(food),
                    restaurant_id=wrap_with_in_single_quote(restaurant_id)
                )
            c.execute(to_execute)
            food_tbl = c.fetchall()
            for r in food_tbl:
                food_id = r[0]
                print(food_id)
                to_execute = "INSERT INTO SELECTED(ORDER_ID,FOOD_ID)" \
                     " VALUES({order_id},{food_id}) "
                to_execute = to_execute.format(
                    order_id=wrap_with_in_single_quote(order_id),
                    food_id=wrap_with_in_single_quote(food_id)
                )
                print(to_execute)
                try:
                    sql.execute(to_execute)
                    contex = 'selected successfully'
                    print(contex)

                except:
                    print("Something is not right. And why rollback is not working.")
                    sql.rollback()
                    # messages.info(request, "adding of foodman was unsuccessfull")

                finally:
                    sql.commit()
        c.close()
            
        #----------------end of selected------------#
    return render(request, 'homeApp/confirm_payment.html', {'customer_name': first_name})
