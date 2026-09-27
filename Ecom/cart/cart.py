from decimal import Decimal
from MyEcom.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        # Drop leftovers from the old cart format ('name', 'items') - only product entries are dicts
        for key in [k for k, v in cart.items() if not isinstance(v, dict)]:
            del cart[key]
            self.session.modified = True
        self.cart = cart  #instance variable to hold the cart data, keyed by product id
   
    def __len__(self):
         # Returns the total number of items in the cart
        return sum(int(item['quantity']) for item in self.cart.values()) 
    
    def get_total_price(self):
        # Returns the total price of all items in the cart
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def __iter__(self):
        # Iterate over the items in the cart and get the products from the database
        # Work on copies so Product/Decimal objects never end up in the session (it must stay JSON)
        cart = {pid: dict(item) for pid, item in self.cart.items()}
        products = Product.objects.filter(id__in=cart.keys())
        for product in products:
            cart[str(product.id)]['product'] = product
            cart[str(product.id)]['quantity_range'] = range(1, product.stock + 1)  # templates have no range()
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item # yield is a generator that convert all the items in a iterable listand yeilds each item in the cart, now enriched with product details and total price
    
    def add(self, product, quantity):
        product_id = str(product.id)  # session is stored as JSON, so keys come back as strings
        quantity = int(quantity)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id] = {'price': str(product.price), 'quantity': quantity}
        self.session.modified = True  # Mark the session as modified to ensure it gets saved

    def delete(self, product_id):
        product_id = str(product_id)  # session keys are strings
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True  # Mark the session as modified to ensure it gets saved
    
    def update(self, product_id, quantity):
        product_id = str(product_id)  # session keys are strings
        quantity = int(quantity)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.session.modified = True  # Mark the session as modified to ensure it gets saved
