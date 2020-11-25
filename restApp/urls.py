from django.urls import path

from . import views

app_name = 'restApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_food/', views.add_food, name='add_food'),
    path('edit_food/', views.edit_food, name='edit_food'),
]
