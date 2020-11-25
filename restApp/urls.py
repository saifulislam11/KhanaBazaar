from . import views
from django.urls import path

app_name = 'restApp'

urlpatterns = [
    path('', views.index, name='index'),
]
