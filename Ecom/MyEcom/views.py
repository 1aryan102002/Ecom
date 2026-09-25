from django.contrib import messages

from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Product

def Hero_home(request):
    products = Product.objects.all()
    return render(request, 'MyEcom/hero_home.html', {'products': products})

def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    quantity_range = range(1, product.stock + 1) if product.stock > 0 else []
    return render(request, 'MyEcom/product_detail.html', {'product': product, 'quantity_range': quantity_range})

def Add_to_cart(request, slug):
    count = request.session.get('cart_count', 0)
    product = Product.objects.get(slug=slug)
    
    if product.stock > 0:
        # Logic to add the product to the cart goes here
        count += 1
        request.session['cart_count'] = count
        
        # Using Django's built-in messages library
        messages.success(request, f"Item added to cart.")
        
    # Redirect back to the page the user was on
    return redirect(request.META.get('HTTP_REFERER', '/'))