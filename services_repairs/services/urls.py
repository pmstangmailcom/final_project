from django.contrib import admin
from django.urls import path
from .views import HelloWorldView

urlpatterns = [
    path('', HelloWorldView, name='Hello')
    ]