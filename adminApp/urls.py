from django.urls import path
from . import views

app_name = 'adminApp'

urlpatterns = [
    path('',views.index, name = 'index' ),
    path('add_restaurant', views.add_restaurant, name ='add_restaurant'),
    path('create_promo', views.create_promo, name = 'create_promo'),
]