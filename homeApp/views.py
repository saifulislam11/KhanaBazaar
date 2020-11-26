from django.shortcuts import render
import cx_Oracle
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.db import connection
from django.http import HttpResponseRedirect

from khanabazaar.settings import MEDIA_URL, MEDIA_ROOT, STATIC_ROOT
from django.shortcuts import render, redirect
from helper.read_write_to_file import handle_uploaded_file
from helper.sql import get_next_id
from helper.wrap_and_encode import wrap_with_in_single_quote, get_hashed_value
from helper import sql
from datetime import datetime,timedelta
con = cx_Oracle.connect("KB", "123", "localhost/orcl")
print("Connected!")
c = con.cursor()
# Create your views here.
def index(request):
    c = con.cursor()
    c.execute('select * from RESTAURANT')
    dict_result = []
    for row in c:
        id=row[0]
        name = row[1]
        path=row[3]
        dic = {'id':id,'name':name,'path':path}
        dict_result.append(dic)
    list1=[]
    list2=[]
    list3=[]
    brk=int(len(dict_result)/3)
    for i in range(len(dict_result)):
        if(int(i/brk) == 0):
            list1.append(dict_result[i])
        elif(int(i/brk) == 1):
            list2.append(dict_result[i])
        else:
            list3.append(dict_result[i])
    c.close()
    

    #-------------logout--------------#
    if request.method =='GET':
        print('get method')
        if 'action' in request.GET:
            action = request.GET.get('action')
            if action == 'logout':
                print('action logout')
                if request.session.has_key('first_name'):
                    print('has key in session')
                    request.session.flush()
                    return render(request,'homeApp/index.html',{'list1':list1,'list2':list2,'list3':list3,'contex':'None'})
    if not request.session.is_empty():
        print('has session while in index')
        if 'first_name' in request.session:
            first_name = request.session['first_name']
        return render(request, 'homeApp/homepage.html',{'list1':list1,'list2':list2,'list3':list3,'customer_name':first_name})

	# connection.commit()
	# cursor.close()
    return render(request,'homeApp/index.html',{'list1':list1,'list2':list2,'list3':list3,'contex':'None'})

#--------------------------after sign in --------------------------#
def homepage(request):
    c = con.cursor()
    c.execute('select * from RESTAURANT')
    dict_result = []
    for row in c:
        id=row[0]
        name = row[1]
        path=row[3]
        dic = {'id':id,'name':name,'path':path}
        dict_result.append(dic)
    list1=[]
    list2=[]
    list3=[]
    brk=int(len(dict_result)/3)
    for i in range(len(dict_result)):
        if(int(i/brk) == 0):
            list1.append(dict_result[i])
        elif(int(i/brk) == 1):
            list2.append(dict_result[i])
        else:
            list3.append(dict_result[i])
    

	# connection.commit()
	# cursor.close()
    #----------------sign in----------------#
    if not request.session.is_empty():
        print('has session')
        if 'first_name' in request.session:
            first_name = request.session['first_name']
        return render(request, 'homeApp/homepage.html',{'list1':list1,'list2':list2,'list3':list3,'customer_name':first_name})
    if request.method == 'POST':
        #------------------sign up-------------#
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email_log = request.POST.get('email')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password')
        password1 = get_hashed_value(password1)
        password2 = request.POST.get('confirmpassword')
        address = request.POST.get('address')
        id = get_next_id()
        #print(firstname+lastname+address)
        if (firstname != None and lastname!=None and email_log!=None) :
            to_execute = "INSERT INTO CUSTOMER(ID,LAST_NAME,FIRST_NAME,EMAIL,PASSWORD_HASH,ADDRESS)" \
                        " VALUES({id}, {lastname}, {firstname}, {email}, {password_hash}, {address}) "
            to_execute_phone = "INSERT INTO CUSTOMER_PHONE(CUSTOMER_ID,PHONE_NO)" \
                        " VALUES({id}, {phone}) "
            to_execute_phone = to_execute_phone.format(
                id=wrap_with_in_single_quote(id),
                phone = wrap_with_in_single_quote(phone)
            )
            to_execute = to_execute.format(
                id=wrap_with_in_single_quote(id),
                firstname=wrap_with_in_single_quote(firstname),
                lastname=wrap_with_in_single_quote(lastname),
                email=wrap_with_in_single_quote(email_log),
                password_hash=wrap_with_in_single_quote(password1),
                address=wrap_with_in_single_quote(address)
            )
            
            info = id + ' ' +firstname +' '+lastname+' '+email_log
            customer_info= info.split(' ')
            print(customer_info)

            #print(firstname+lastname+address)
            print(to_execute)
            try:
                sql.execute(to_execute)
                sql.execute(to_execute_phone)
                contex = 'registered successfully'
                return render(request,'homeApp/index.html',{'list1':list1,'list2':list2,'list3':list3,'contex':contex})
            
            except:
                print("Something is not right. And why rollback is not working.")
                sql.rollback()
                #messages.info(request, "adding of foodman was unsuccessfull")
                return render(request,'homeApp/index.html',{'list1':list1,'list2':list2,'list3':list3,'contex':'something went wrong.try again'})

            finally:
                c.close()
                sql.commit()
                
            #return render(request, 'homeApp/homepage.html',{'list1':list1,'list2':list2,'list3':list3,'customer':customer_info,'customer_name':firstname})
        if lastname == None :
            #---------------------sign up--------------------#
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
                return render(request, 'homeApp/index.html',{'list1':list1,'list2':list2,'list3':list3,'contex':'None'})
            else:
                print('We need to do something')
                id = customer[0]
                last_name = customer[1]
                first_name = customer[2]
                request.session['id'] = id
                request.session['last_name'] = last_name
                request.session['first_name'] = first_name
                request.session['email'] = email
                #info = id + ' ' +firstname +' '+lastname+' '+email
                #customer_info= info.split(' ')

                return render(request, 'homeApp/homepage.html',{'list1':list1,'list2':list2,'list3':list3,'customer':customer,'customer_name':customer[2]})
        else:
            return redirect('/homepage')
    else:
        print('couldnt fetch post method')
        return render(request, 'homeApp/index.html',{'list1':list1,'list2':list2,'list3':list3,'contex':'None'})
    c.close()
    #---------------------end of sign in ------------------#


        
    

#--------------------customer register-------------------#
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
    return render(request,'homeApp/aboutus.html')
def contactus(request):
    return render(request,'homeApp/contactus.html')
#payment method
def payment(request):
    c = con.cursor()
    price=request.POST.get('price')
    foods = request.POST.get('foods')
    prices = request.POST.get('prices')
    counts = request.POST.get('counts')
    restaurant=request.POST.get('restaurant')
    items=request.POST.get('items')
    food_collections=foods.split("#")
    count_collections=counts.split("#")
    price_collections=prices.split("#")
    ##removing last element
    all_food=[]
    all_count=[]
    all_price=[]
    for i in range(len(food_collections)-1):
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
    sql="select * from RESTAURANT WHERE ID= %s" % restaurant

    c.execute(sql)
    
    
    for row in c :
        id=row[0]
        name=row[1]
        path=row[3]
        rest_dic={'id':id,'name':name,'path':path}
        
    print(rest_dic)
    cart_dic=[]
    for i in range(len(all_food)):
        food=all_food[i]
        amount=all_price[i]
        count=all_count[i]
        dic={'food':food,'price':amount,'count':count}
        cart_dic.append(dic)
    print(cart_dic)
    c.close()
    #info from session
    if 'first_name' in request.session:
        first_name = request.session['first_name']
    if 'id' in request.session:
        id = request.session['id']
    if 'last_name' in request.session:
        last_name = request.session['last_name']
    if 'email' in request.session:
        email = request.session['email']

    


    
    return render(request,'homeApp/payment.html',{'price':price,'items':len(cart_dic),'restaurant':rest_dic,'cart':cart_dic,'customer_name':first_name,'last_name':last_name,'email':email})

def restaurant(request):
    c = con.cursor()
    c.execute('select * from RESTAURANT')
    query=None
    results=None
    email = None
    password = None
    if request.method == 'POST':
        query = request.POST.get('restaurant')
        email = request.POST['email']
        password = request.POST['password']
        print('chole')
        
        print(query)
        test=0
        for row in c:
            #print(row[1])
            if len(query)==0 or str(row[1].lower()).find(str(query.lower()))==-1:
                test=0

            elif str(row[1].lower()).find(str(query.lower()))!=-1:
                results=row[3]
                title=row[1]
                REST_id=row[0]
                test=1
                id=row[0]
                break
                
                #print(row[3])
        print(test)
        if test==0:
            c.close()
            return render(request,'homeApp/restaurant.html',{'path':None})
        else:
            print(type(id))
            print(id)
            command="select * from FOOD_ITEM WHERE RESTAURANT_ID = %s" % id
            c.execute(command)
            foods=c.fetchall()
            
            dict_result = []
            types=[]
            for row in foods:
                id=row[0]
                id=str(id)
                command="select * from FOOD_ITEM_PATH WHERE ID = %s" % id
                c.execute(command)
                food_path=c.fetchall()
                path=None
                for r in food_path:
                    path=r[1]
                name = row[2]
                price=row[3]
                food_type=row[7]
                print(id+' '+name+' '+food_type+' '+path)
                types.append(food_type)
                dic = {'id':id,'name':name,'price':price,'type':food_type,'path':path}
                dict_result.append(dic)
            types_set=set(types)
            unique_types= list(types_set)
            c.close()
            if not request.session.is_empty():
                print('has session')
                if 'first_name' in request.session:
                    first_name = request.session['first_name']
                if 'id' in request.session:
                    id = request.session['id']
                if 'last_name' in request.session:
                    last_name = request.session['last_name']
                if 'email' in request.session:
                    email = request.session['email']
                customer_dict = {'id':id,'last_name':last_name,'first_name':first_name,'email':email}
                print(customer_dict)
                return render(request, 'homeApp/restaurant.html',{'path':results,'ID':REST_id,'title':title,'foods':dict_result,'all_types':unique_types,'customer_name':first_name,'customer_dic':customer_dict})
            elif email =="None" or password == "None" :
                return render(request,'homeApp/restaurant_log_in.html',{'path':results,'ID':REST_id,'title':title,'foods':dict_result,'all_types':unique_types,'customer_name':'none'})
            else:
                print(email+' '+password)
                #c.close()
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
                    return render(request,'homeApp/restaurant_log_in.html',{'path':results,'ID':REST_id,'title':title,'foods':dict_result,'all_types':unique_types,'customer_name':'none'})
                else:
                    print('We need to do something')
                    id = customer[0]
                    last_name = customer[1]
                    first_name = customer[2]
                    email = customer[3]
                    address = customer[5]
                    customer_dict = {'id':id,'last_name':last_name,'first_name':first_name,'email':email,'address':address}
                    print(customer_dict)
                    request.session['id'] = id
                    request.session['last_name'] = last_name
                    request.session['first_name'] = first_name
                    request.session['email'] = email
                    #info = id + ' ' +firstname +' '+lastname+' '+email
                    #customer_info= info.split(' ')

                    return render(request, 'homeApp/restaurant.html',{'path':results,'ID':REST_id,'title':title,'foods':dict_result,'all_types':unique_types,'customer_name':first_name,'customer_dic':customer_dict})
                #return render(request,'homeApp/restaurant_log_in.html',{'path':results,'ID':REST_id,'title':title,'foods':dict_result,'all_types':unique_types,'customer_name':'none'})

def confirm_payment(request):
    c = con.cursor()
    if 'first_name' in request.session:
        first_name = request.session['first_name']
    if 'id' in request.session:
        id = request.session['id']
    if 'last_name' in request.session:
        last_name = request.session['last_name']
    if 'email' in request.session:
        email = request.session['email']
    if request.method == 'POST':
        order_price = request.POST.get('order_price')
        delivery_type = request.POST.get('delivery_type')
        delivery_location = request.POST.get('delivery_address')
        print(order_price+' '+delivery_location+' '+delivery_type)
        now = datetime.now()
        order_time = now.strftime("%d/%m/%Y %H:%M:%S")
        print(order_time)
        delivery_time = now + timedelta(hours=2)
        delivery_time = delivery_time.strftime("%d/%m/%Y %H:%M:%S")
        print(delivery_time)
        id = get_next_id()
        table_name ='"' + "ORDER"+ '"'
        print(table_name)
        to_execute = "INSERT INTO {table_name}(ID,ORDER_TIME,DELIVERY_TIME,DELIVERY_LOCATION)" \
                        " VALUES({id}, to_date({order_time},'DD/MM/YYYY HH:MI:SS'), to_date({delivery_time},'DD/MM/YYYY HH:MI:SS'), {delivery_location}) "
        to_execute = to_execute.format(
            table_name = "{}".format(table_name),
            id=wrap_with_in_single_quote(id),
            order_time=wrap_with_in_single_quote(order_time),
            delivery_time=wrap_with_in_single_quote(delivery_time),
            delivery_location=wrap_with_in_single_quote(delivery_location)
        )
        
        info = id + ' ' +delivery_time +' '+order_time+' '+delivery_location
        order_info= info.split(' ')
        print(order_info)

        #print(firstname+lastname+address)
        print(to_execute)
        try:
            sql.execute(to_execute)
            contex = 'ordered successfully'
            return render(request,'homeApp/confirm_payment.html',{'customer_name':first_name})
        
        except:
            print("Something is not right. And why rollback is not working.")
            sql.rollback()
            #messages.info(request, "adding of foodman was unsuccessfull")
            return render(request,'homeApp/confirm_payment.html',{'customer_name':first_name})

        finally:
            c.close()
            sql.commit()
    return render(request,'homeApp/confirm_payment.html',{'customer_name':first_name})





    
    


    