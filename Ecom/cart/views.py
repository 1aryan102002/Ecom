from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
def cart_add(request):
    print("Adding product to the cart.")
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        print(f"Received product_id: {product_id}, quantity: {quantity}")
        # Here you would typically add the product to the cart in the session or database
    return JsonResponse({'message': 'success'})