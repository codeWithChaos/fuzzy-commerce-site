from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart


# @login_required(login_url='/login/')
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)

@login_required(login_url='/login/')
def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        
        if form.is_valid():
            form.save()
            
            messages.success(request, 'You have successfully registered! :)')
            return redirect('home')
        return render(request, 'store/update_info.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in to access that page :(')
        return render(request, 'store/update_info.html', {'form': form})

def category(request, category_name):
    """
    Display products for a specific category.
    """
    category_name = category_name.replace('-', ' ')  # Replace hyphens with spaces
    # Grab the category from the url
    try:
        # Look up the category
        category = Category.objects.get(name__iexact=category_name)  # Case-insensitive match
        categories = Category.objects.all()
        products = Product.objects.filter(category=category)
        return render(request, 'store/category.html',  {'products': products, 'category': category, 'categories': categories})
    except Category.DoesNotExist:
        messages.error(request, f'The category "{category_name}" does not exist.')
        return redirect('home')

def product(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product': product
    }
    return render(request, 'store/product.html', context)

def about(request):
    return render(request, 'store/about.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # Get their saved cart from db
            saved_cart = current_user.old_cart
            # convert db string to python dictionary
            if saved_cart:
                # convert to dictionary using json
                converted_cart = json.loads(saved_cart)
                # Add the loaded cart dictionay to our session
                cart = Cart(request)
                # Loop through the cart and add the items from the db
                for key, value in converted_cart.items():
                    cart.db_cart(product=key, quantity=value)
            
            messages.success(request, 'You have been logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    else:
        return render(request, 'store/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out. Thanks for stopping by! 😊')
    return redirect('home')

def register(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Username Created - Please Fill Out Your User Info Below!')
            return redirect('update-info')
        else:
            messages.error(request, 'An error occurred during registration.')
            return redirect('register')
    else:
        return render(request, 'store/register.html', {'form': form})

@login_required(login_url='/login/')
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        
        if user_form.is_valid():
            user_form.save()
            
            login(request, current_user)
            messages.success(request, 'User has been updated')
            return redirect('home')
        return render(request, 'store/update_user.html', {'user_form': user_form})
    else:
        messages.error(request, 'You must be logged in to access that page.')
        return redirect('home')

@login_required(login_url='/login/')
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form?
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your Password has been updated...')
                return redirect('update-user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update-password')
        else:
            form = ChangePasswordForm(current_user)
    else:
        messages.error(request, 'You must be logged in to view that page.')
    return render(request, 'store/update_password.html', {'form': form})
    
def category_summary(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'store/category_summary.html', context)

def search(request):
    # Determine if they fill out the form
    if request.method == 'POST':
        searched = request.POST.get('search')
        # Query the Product model
        searched_product = Product.objects.filter(
            Q(name__icontains=searched) | Q(description__icontains=searched)
        )
        # Test for null
        if not searched_product:
            messages.error(request, 'That Product does not exist.')
            return render(request, 'store/search.html', {})
        else:
            return render(request, 'store/search.html', {'searched': searched_product})
    return render(request, 'store/search.html', {})