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
        
        