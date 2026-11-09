from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home' ),
    path('about/', views.about, name='about'),
    path('cart/', views.cart_detail, name='cart'),
    path('cart/increment/<int:product_id>/', views.cart_increment, name='cart_increment'),
    path('cart/decrement/<int:product_id>/', views.cart_decrement, name='cart_decrement'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/buy/<int:product_id>/', views.cart_add_and_buy, name='cart_add_and_buy'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('product/<slug:slug>/', views.Product_details, name='product_detail'),
    path('create_order', views.create_order, name='create_order'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order_success/', views.order_success_view, name='order_success'),
    ]