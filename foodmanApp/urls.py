from django.urls import path
from . import views


app_name = 'foodmanApp'

urlpatterns = [
    path('', views.index, name = 'index'),
]