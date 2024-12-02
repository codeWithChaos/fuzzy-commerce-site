from store.models import Product


class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get the current session key
        cart = self.session.get('session_key')
        # If user is new, create a new session key
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages
        self.cart = cart
    
    def add(self, product, quantity):
        product_id = str(product.id)
        product_quantity = str(quantity)
        
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'Price ': str(product.price)}
            self.cart[product_id] = int(product_quantity)
        
        self.session.modified = True
        
    def __len__(self):
        return len(self.cart)
    
    def get_products(self):
        # Get the product IDs
        product_ids = self.cart.keys()
        
        # Use the product IDs to get the products
        products = Product.objects.filter(id__in=product_ids)
        
        return products
    
    def get_quantities(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_quantity = int(quantity)
        
        # Grab our cart
        our_cart = self.cart
        
        # Update Dictionary/cart
        our_cart[product_id] = product_quantity
        # if product_id in self.cart:
        #     self.cart[product_id] = int(product_quantity)

        self.session.modified = True
        
        thing = self.cart
        return thing
    
    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True