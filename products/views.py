"""Import models"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
# from django.contrib.auth.models import User
from .models import Product
from .models import Cart

# Create your views here.


def home(request):
    """ Render product page """
    pds = Product.objects.all()
    return render(request, 'product.html', {'products': pds})


def product_details(request, pid):
    in_cart = Cart.objects.filter(user=request.user.username, product_id=pid).values('product_id', 'user').annotate(quantity=Sum('quantity'))
    quantity = 0
    if in_cart:
        quantity = in_cart.get(product_id=pid).get('quantity')
    product = Product.objects.get(product_id=pid)
    return render(request, 'details.html', {'product': product, 'quantity': quantity})


def product_cart(request, pid):

    storage = messages.get_messages(request)
    storage.used = True

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
    product_stock = product_get.quantity_in_stock
    price = product_get.sell_price

    in_cart = Cart.objects.filter(user=request.user.username, product_id=pid).values('product_id', 'user').annotate(quantity=Sum('quantity'))
    cart_quantity = 0
    if in_cart:
        cart_quantity = in_cart.get(product_id=pid).get('quantity')

    if quantity != 0 and user != "none":
        if int(quantity) + cart_quantity > product_stock:
            messages.add_message(request, messages.INFO, "Heyyyy! You know we do not have that many right?")
        else:
            messages.add_message(request, messages.INFO, 'You have added a product to your cart!')
            product_in = Cart(product_id=product_id, product_name=product_name, quantity=quantity, price=price, user=user)
            product_in.save()
    else:
        messages.add_message(request, messages.INFO, 'Oops!')

    return redirect('/products')


def cart_get(request):
    cart = Cart.objects.filter(user=request.user.username).values('product_id', 'product_name', 'product_image', 'price', 'user').annotate(quantity=Sum('quantity'))
    total_price = 0
    for cart_data in cart:
        total_price += cart_data.get('price') * cart_data.get('quantity')
    return render(request, 'cart.html', {'cart': cart, 'total': total_price})
