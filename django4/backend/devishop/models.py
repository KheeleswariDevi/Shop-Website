from django.db import models 
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.shortcuts import render


class User(AbstractUser):
    User = get_user_model

    pass



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.FileField(upload_to='products', blank=True, null=True)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} in {self.basket.user.username}'s basket"


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE) 
    # product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    # quantity = models.PositiveIntegerField()
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"

    def calculate_total_price(self):
        self.total_price = sum(item.product.price * item.quantity for item in self.items.all())
        self.save()

from django.views.generic import TemplateView

class About_us(TemplateView):
    def get(self, request):
        return render(request, 'about_us.html')

