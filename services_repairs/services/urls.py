from django.contrib import admin
from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.all_orders, name='all_orders'),
    path('order/<int:id>', views.order_details, name='order_details'),
    path('new_order/', views.add_new_order, name='add_new_order'),


    path('update/<int:id>/', views.update_order, name='update_order'),
    path('delete/<int:id>', views.delete_order, name='delete_order'),

    path('user/', views.user_orders, name='user_orders'),
    path('executor/', views.new_executor, name='new_executor'),


    ]