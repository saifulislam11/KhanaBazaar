from django.urls import path
from . import views

app_name = 'adminApp'

urlpatterns = [
    path('',views.signIn, name = 'signin' ),
]