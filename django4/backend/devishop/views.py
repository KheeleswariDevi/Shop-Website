from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Basket, BasketItem
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import CustomUserCreationForm, CheckoutForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CheckoutForm 
from .models import Order, OrderItem
from collections import defaultdict
from .models import Category


def index(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category_id:
        products = products.filter(category__id=category_id)

    categories = Category.objects.all()

    return render(request, 'index.html', {
        'products': products,
        'categories': categories,
        'query': query,  
        'user': request.user
    })

def product_individual(request, prodid):
    product = get_object_or_404(Product, id=prodid)
    return render(request, 'product_detail.html', {'product': product})



@login_required
def basket(request):
    basket, created = Basket.objects.get_or_create(user=request.user, is_active=True)

    products = basket.basketitem_set.all() 

    total_price = sum(item.product.price * item.quantity for item in products)  

    return render(request, 'basket.html', {
        'products': products,
        'total_price': total_price
    })


@login_required
def add_to_basket(request, prodid):
    product = get_object_or_404(Product, id=prodid)
    basket, created = Basket.objects.get_or_create(user=request.user, is_active=True)

    basket_item, item_created = BasketItem.objects.get_or_create(basket=basket, product=product)

    if not item_created:
        basket_item.quantity += 1
    basket_item.save()


    messages.success(request, f'{product.name} has been added to your basket.')

    return redirect('index')


@login_required
def remove_from_basket(request, product_id):
    if request.method == 'POST':
        basket = Basket.objects.get(user=request.user, is_active=True)
        try:
            basket_item = basket.basketitem_set.get(product__id=product_id)

            if basket_item.quantity > 1:
                basket_item.quantity -= 1
                basket_item.save()
            else:
                basket_item.delete() 

            return redirect('basket')
        except BasketItem.DoesNotExist:
            messages.error(request, "Item not found in your basket.")
            return redirect('basket')

    return redirect('basket') 


@login_required
def add_quantity(request, product_id):
    if request.method == 'POST':
        basket = Basket.objects.get(user=request.user, is_active=True)
        try:
            basket_item = basket.basketitem_set.get(product__id=product_id)

            basket_item.quantity += 1
            basket_item.save()

            return redirect('basket')
        except BasketItem.DoesNotExist:
            messages.error(request, "Item not found in your basket.")
            return redirect('basket')

    return redirect('basket')


def basket_view(request):
    basket_items = BasketItem.objects.filter(basket__user=request.user)
    for item in basket_items:
        item.item_total = item.product.price * item.quantity
    context = {
        'basket_items': basket_items,
    }
    return render(request, 'basket.html', context)


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm  # Adjust the import if needed

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login') 
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("User authenticated and logged in.")
            return redirect('index') 
        else:
            print("Invalid login attempt.")
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')  



@login_required
def order_confirmation(request):
    try:
        latest_order = Order.objects.filter(user=request.user).latest('ordered_at')
        total_price = sum(item.product.price * item.quantity for item in latest_order.items.all())

        return render(request, 'order_confirmation.html', {
            'order': latest_order,
            'order_items': latest_order.items.all(),
            'total_price': total_price,
        })

    except Order.DoesNotExist:
        return render(request, 'order_confirmation.html', {
            'message': 'No recent order found.'
        })




@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')

    grouped_orders = defaultdict(list)
    for order in orders:
        order_date = order.ordered_at.date()
        total_price = sum(item.product.price * item.quantity for item in order.items.all())
        grouped_orders[order_date].append((order, total_price))

    return render(request, 'order_history.html', {
        'grouped_orders': grouped_orders.items(), 
    })



@login_required
def checkout_view(request):
    basket, created = Basket.objects.get_or_create(user=request.user, is_active=True)
    basket_items = BasketItem.objects.filter(basket=basket)

    if not basket_items.exists():
        messages.error(request, "Your basket is empty. Please add items before checking out.")
        return redirect('basket')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order(user=request.user)
            order.save() 

    
            for item in basket_items:
                OrderItem.objects.create(
                    order=order,  
                    product=item.product,
                    quantity=item.quantity
                )

            basket.is_active = False
            basket.save()

            return redirect('order_confirmation')

    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {
        'form': form,
        'basket_items': basket_items,
    })


def logout_confirmation(request):
    if request.method == 'POST': 
        logout(request)
        return redirect('index')  
    return render(request, 'logout_confirmation.html')


def about_us(request):
    return render(request, 'about_us.html')

def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())