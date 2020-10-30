from django.urls import path
from . import views

app_name = 'adminApp'

urlpatterns = [
    path('',views.index, name = 'index' ),
    path('addRestaurant', views.addRestaurant, name = 'addRestaurant'),
]