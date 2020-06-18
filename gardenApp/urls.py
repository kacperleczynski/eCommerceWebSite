from django.contrib import admin
from django.urls import path, include
from gardenApp import views


app_name = 'gardenApp'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('contact/', views.contact, name = 'contact'),
    path('about_us/', views.about_us, name = 'about_us'),
    path('shop/', views.shop, name = 'shop'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('store/', views.store, name = 'store'),
    path('cart/', views.cart, name = 'cart'),
    path('update_item/', views.updateItem, name = 'update_item'),
    path('process_order/', views.processOrder, name = 'process_order')

]
