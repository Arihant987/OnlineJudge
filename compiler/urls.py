from django.contrib import admin
from django.urls import path, include
from compiler import views

urlpatterns =  [
    path('',views.submit,name='submit'),
]

