from django.shortcuts import render
from django.http import JsonResponse
from .cart import Cart
from MyEcom.models import Product
from django.shortcuts import get_object_or_404
# Create your views here.
def cart_add(request):
    cart = Cart(request)
    print("Adding product to the cart.")
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        print(f"Received product_id: {product_id}, quantity: {quantity}")
        # Here you would typically add the product to the cart in the session or database
       # product = Product.objects.get(id=product_id)
        product = get_object_or_404(Product, id=product_id) 
        cart.add(product = product, quantity=quantity)
    # Computed outside the if-block so it always exists, even for non-POST requests
    cart_qty = len(cart)
    return JsonResponse({'message': 'success', 'cart_qty': cart_qty})