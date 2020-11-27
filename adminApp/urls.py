from django.urls import path
from . import views

app_name = 'adminApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_restaurant', views.add_restaurant, name='add_restaurant'),
    path('create_promo', views.create_promo, name='create_promo'),
    path('add_foodman', views.add_food_man, name='add_foodman'),
    path('edit_restaurant', views.edit_restaurant, name='edit_restaurant'),
]
