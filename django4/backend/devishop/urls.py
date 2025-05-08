from django.urls import path
from . import views
from .views import logout_confirmation
from .views import (
    index,
    product_individual,
    add_to_basket,
    basket,
    remove_from_basket,
    register,
    user_login,
    checkout_view,
    user_logout,
    order_confirmation,
    order_history,
    about_us
)


urlpatterns = [
   path('', views.index, name="index"),
   path('products/<int:prodid>/', views.product_individual, name="individual_product"),
   path('addbasket/<int:prodid>/', views.add_to_basket, name="add_basket"),
   path('basket/', views.basket, name='basket'),
   path('removebasket/<int:product_id>/', remove_from_basket, name='remove_from_basket'),
   path('register/', views.register, name='register'),
   path('checkout/', checkout_view, name='checkout'),
   path('logout/', views.user_logout, name='logout'),
   path('login/', views.user_login, name='login'), 
   path('logout_confirmation/', views.logout_confirmation, name='logout'),
   path('order-confirmation/', views.order_confirmation, name='order_confirmation'),  
   path('order-history/', views.order_history, name='order_history'),
   path('product/<int:prodid>/', views.product_individual, name='individual_product'),
   path('add_quantity/<int:product_id>/', views.add_quantity, name='add_quantity'),
   path('about-us/', views.about_us, name='about_us'),
]
