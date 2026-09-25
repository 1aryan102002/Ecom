
from django.urls import path
from MyEcom import views  # Import your app's views

urlpatterns = [
    
    path('', views.Hero_home, name='hero_home'),  # Matches the root URL (http://127.0.0.1:8000/)
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),  # Matches product detail URLs (http://127.0.0.1:8000/product/slug/)
    path('add-to-cart/<slug:slug>/', views.Add_to_cart, name='add_to_cart'),  # Matches add to cart URLs (http://127.0.0.1:8000/add-to-cart/slug/)
]
