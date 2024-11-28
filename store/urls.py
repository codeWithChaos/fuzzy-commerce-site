from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('product/<int:pk>/', views.product, name='product_detail'),
    path('category/<str:category_name>/', views.category, name='category'),
]