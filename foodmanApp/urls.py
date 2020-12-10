from django.urls import path

app_name = 'foodmanApp'
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('current_order/', views.current_order, name='current_order'),
    path('accept_order/', views.accept_order, name='accept_order'),
    path('add_phone/', views.add_phone, name = 'add_phone'),
]
