from .cart import Cart


# Create context processor so the cart can work on all pages of site
def cart(request):
    # Return the default data from our cart
    return {'cart': Cart(request)}