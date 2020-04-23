"""Import models"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Product
from .models import Cart

# Create your views here.


def home(request):
    """ Render product page """
    pds = Product.objects.all()
    return render(request, 'product.html', {'products': pds})

def product_details(request, pid):
    product = Product.objects.get(product_id=pid)
    return render(request, 'details.html', {'product': product})

def product_cart(request, pid):

    if request.method == 'POST':
        quantity = request.POST['quantity']
    else:
        quantity = 0

    if request.user.is_authenticated:
        user = request.user.username
    else:
        user = "none"

    product_get = Product.objects.get(product_id=pid)
    product_id = product_get.product_id
    product_name = product_get.product_name
    product_image = product_get.product_image
    price = product_get.sell_price
    
    if quantity != 0 and user != "none" :
        messages.add_message(request, messages.INFO, 'You have added a product to your cart!')
        product_in = Cart(product_id=product_id, product_name=product_name, quantity=quantity, price=price, user=user)
        product_in.save()
    
    messages.add_message(request, messages.INFO, 'Oops!')
    return redirect('/products')


def cart_get(request):
    cart = Cart.objects.all()
    return render(request, 'cart.html', {'cart': cart})
