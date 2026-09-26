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
    
    def add(self, product, quantity):
        product_id = str(product.id)  # session is stored as JSON, so keys come back as strings
        quantity = int(quantity)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id] = {'price': str(product.price), 'quantity': quantity}
        self.session.modified = True  # Mark the session as modified to ensure it gets saved
