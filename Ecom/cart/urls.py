from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.cart_add, name='cart_add'),
    path('cart-detail/', views.cart_detail, name='cart_detail'),
    path('delete/', views.cart_delete, name='cart_delete'),
    path('update/', views.update_cart, name='update_cart'),
]