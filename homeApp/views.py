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
def restaurant(request):
    c.execute('select * from RESTAURANT')
    query=None
    results=None
    if request.method == 'POST':
        query = request.POST.get('restaurant')
        print(query)
        for row in c:
            print(row[1])
            if str(row[1].lower()).find(str(query.lower()))!=-1:
                results=row[3]
                print(row[3])
    
    


    return render(request,'homeApp/restaurant.html',{'path':results})