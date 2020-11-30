from django.urls import path

app_name = 'restApp'

from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('add_food/', views.add_food, name='add_food'),
    path('edit_food/', views.edit_food, name='edit_food'),
    path('edit_particular_food/', views.edit_particular_food, name='edit_particular_food'),
    path('update_time/', views.update_time, name='update_time'),
    path('update_logo/', views.update_logo, name='update_logo'),
    path('update_location/', views.update_location, name='update_location'),
]
