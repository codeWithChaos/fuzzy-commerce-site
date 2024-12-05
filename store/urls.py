from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('update_user/', views.update_user, name='update-user'),
    path('product/<int:pk>/', views.product, name='product_detail'),
    path('category/<str:category_name>/', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category-summary'),
    path('update_password/', views.update_password, name='update-password'),
    path('update_info/', views.update_info, name='update-info'),
]