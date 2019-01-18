from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='keep_main'),
    path('order_list/', views.home, name='order_list'),
]
