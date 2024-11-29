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
    
    def add(self, product):
        product_id = str(product.id)
        
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'Price ': str(product.price)}
        
        self.session.modified = True