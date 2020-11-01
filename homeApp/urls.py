from django.urls import path
from . import views

###registering appname to hyperlink in htmls
app_name = 'homeApp'


urlpatterns = [
    path('',views.index,name="index"),
    path("aboutus",views.aboutus,name="aboutus"),
    path("contactus",views.contactus,name="contactus"),
    path("restaurant",views.restaurant,name="restaurant"),
    path("payment",views.payment,name="payment")
    
]
