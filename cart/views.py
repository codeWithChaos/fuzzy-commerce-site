from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def cart_summary(request):
    # Get cart
    cart = Cart(request)
    cart_products = cart.get_products()  # Retrieving the products in the cart
    quantities = cart.get_quantities() # Get the quantities of each product
    totals = cart.cart_total()
    
    context = {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals
    }
    return render(request, 'cart/cart_summary.html', context)

def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # Test for post
    if request.POST.get('action') == 'post':
        
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))
        
        # Look up product in the database
        product = get_object_or_404(Product, id=product_id)
        
        # Save to session
        cart.add(product=product, quantity=product_quantity)
        
        # Get cart quantity
        cart_quantity = cart.__len__()
        
        # Retrun response
        # response = JsonResponse({'Product Name ': product.name})
        response = JsonResponse({'qty ': cart_quantity})
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        
        # Call delete method on the cart
        cart.delete(product=product_id)
        
        response = JsonResponse({'producty ': product_id})
        return response


def cart_update(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        cart.update(product=product_id, quantity=product_quantity)

        response = JsonResponse({'qty ': product_quantity})
        return response


