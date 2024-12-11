from store.models import Product, Profile


class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get request
        self.request = request

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
        
        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the profile model
            current_user.update(old_cart=str(carty))
        
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
        
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))
        return thing
    
    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))
        
    def cart_total(self):
        """
        Calculate the total price of all items in the cart.
        """
        product_ids = self.cart.keys()  # Retrieving the products IDs
        products = Product.objects.filter(id__in=product_ids)  # Retrieving the products
        quantities = self.get_quantities()  # Get quantities of each product in the cart

        total_price = sum(
            (product.sale_price if product.is_sale else product.price) * quantities.get(str(product.id), 0) for product in products
        )

        return total_price
        
        # total = 0
        
        # for key, value in quantities.items():
        #     # key = int(key)
            
        #     for product in products:
        #         if product.id == int(key):
        #             total += product.price * value
        # return total
        
    def db_cart(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
            
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))