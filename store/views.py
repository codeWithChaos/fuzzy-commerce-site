from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm
from django import forms


@login_required(login_url='/login/')
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)

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
    return redirect('login')

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
            messages.success(request, 'You have successfully registered!')
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration.')
            return redirect('register')
    else:
        return render(request, 'store/register.html', {'form': form})
    
def category_summary(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'store/category_summary.html', context)