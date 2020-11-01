from django.shortcuts import render
import cx_Oracle
con = cx_Oracle.connect("KB", "123", "localhost/orcl")
print("Connected!")
c = con.cursor()
# Create your views here.
def index(request):
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
	
    return render(request,'homeApp/index.html',{'list1':list1,'list2':list2,'list3':list3})

def aboutus(request):
    return render(request,'homeApp/aboutus.html')
def contactus(request):
    return render(request,'homeApp/contactus.html')
#payment method
def payment(request):
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

    
    return render(request,'homeApp/payment.html',{'price':price,'items':len(cart_dic),'restaurant':rest_dic,'cart':cart_dic})
def restaurant(request):
    c.execute('select * from RESTAURANT')
    query=None
    results=None
    if request.method == 'POST':
        query = request.POST.get('restaurant')
        
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
            return render(request,'homeApp/restaurant.html',{'path':None})
        else:
            print(type(id))
            print(id)
            sql="select * from FOOD_ITEM WHERE RESTAURANT_ID = %s" % id
            c.execute(sql)
            foods=c.fetchall()
            
            dict_result = []
            types=[]
            for row in foods:
                id=row[0]
                id=str(id)
                sql="select * from FOOD_ITEM_PATH WHERE ID = %s" % id
                c.execute(sql)
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

            return render(request,'homeApp/restaurant.html',{'path':results,'ID':REST_id,'title':title,'foods':dict_result,'all_types':unique_types})


    
    


    