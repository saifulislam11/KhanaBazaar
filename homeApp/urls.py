from django.urls import path

###registering appname to hyperlink in htmls
app_name = 'homeApp'
from . import views




urlpatterns = [
    path('',views.index,name="index"),
    path("aboutus",views.aboutus,name="aboutus"),
    path("contactus",views.contactus,name="contactus"),
    path("restaurant",views.restaurant,name="restaurant"),
    path("payment",views.payment,name="payment"),
    path("homepage",views.homepage,name="homepage"),
    path("restaurant_log_in",views.restaurant,name="restaurant_log_in"),
    path("confirm_payment",views.confirm_payment,name="confirm_payment"),
    path("confirm_foodman",views.confirm_foodman,name="confirm_foodman")


    
]
