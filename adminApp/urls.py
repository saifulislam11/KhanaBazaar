app_name = 'adminApp'
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_restaurant', views.add_restaurant, name='add_restaurant'),
    path('create_promo', views.create_promo, name='create_promo'),
    path('add_foodman', views.add_food_man, name='add_foodman'),
    path('edit_restaurant', views.edit_restaurant, name='edit_restaurant'),
    path('offer_promo/', views.offer_promo, name='offer_promo'),
    path('suspend_customer/', views.suspend_customer, name='suspend_customer'),
    path('suspend_foodman/', views.suspend_foodman, name='suspend_foodman')

]
