from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .forms import ShippingForm
from .models import ShippingAddress
from django.contrib import messages


def payment_success(request):
    return render(request, 'payment/payment_success.html', {})

@login_required(login_url='/login/')
def checkout(request):
    # Get cart
    cart = Cart(request)
    cart_products = cart.get_products()  # Retrieving the products in the cart
    quantities = cart.get_quantities() # Get the quantities of each product
    totals = cart.cart_total()
    try:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    except Exception as e:
        messages.error(request, f'An unexpected error occured: {str(e)}')
        return redirect('home')
    
    context = {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals,
        'shipping_form': shipping_form,
    }
    return render(request, 'payment/checkout.html', context)