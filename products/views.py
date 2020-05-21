"""Import models"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, Q
# from django.contrib.auth.models import User
from .models import Product, Cart, OrderDJ, OrderDetailsDJ

# Create your views here.


def home(request):
    """ Render product page """
    pds = Product.objects.all()
    return render(request, 'product.html', {'products': pds, 'count': pds.count()})


def search(request):
    pds = Product.objects.all()

    if 'pname' in request.GET:
        pname = request.GET["pname"]
        pds = pds.filter(product_name__icontains=pname)

    if 'filter' in request.GET:
        availability = request.GET["filter"]
        if availability == 'avail':
            pds = pds.filter(~Q(quantity_in_stock=0))
        elif availability == 'sold-out':
            pds = pds.filter(quantity_in_stock=0)

    if 'sort' in request.GET:
        sort = request.GET["sort"]
        if sort == 'name-a-to-z':
            pds = pds.order_by('product_name')
        elif sort == 'name-z-to-a':
            pds = pds.order_by('-product_name')
        elif sort == 'price-up':
            pds = pds.order_by('sell_price')
        elif sort == 'price-down':
            pds = pds.order_by('-sell_price')

    return render(request, 'product.html', {'products': pds, 'count': pds.count()})


def product_details(request, pid):
    in_cart = Cart.objects.filter(user=request.user.username, product_id=pid).values('product_id', 'user').annotate(quantity=Sum('quantity'))
    quantity = 0
    if in_cart:
        quantity = in_cart.get(product_id=pid).get('quantity')
    product = Product.objects.get(product_id=pid)
    return render(request, 'details.html', {'product': product, 'quantity': quantity})


def product_cart(request, pid):
    # delete old messages
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
    product_image = product_get.product_image
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
            product_in = Cart(product_id=product_id, product_name=product_name, product_image=product_image, quantity=quantity, price=price, user=user)
            product_in.save()
    else:
        messages.add_message(request, messages.INFO, 'Oops!')

    return redirect('/products')


def cart_get(request):
    cart = Cart.objects.filter(user=request.user.username).values('product_id', 'product_name', 'product_image', 'price', 'user').annotate(quantity=Sum('quantity'))
    stock_changed = False
    for item in cart:
        in_stock = Product.objects.get(product_id=item.get('product_id')).quantity_in_stock
        # If empty stock, remove entry from cart
        if in_stock == 0:
            Cart.objects.filter(user=request.user.username, product_id=item.get('product_id')).delete()
            stock_changed = True
        # Else, change the quantity of that entry in cart
        elif item.get('quantity') > in_stock:
            Cart.objects.filter(user=request.user.username, product_id=item.get('product_id')).update(quantity=in_stock)
            stock_changed = True

    # EDIT: Now print message directly in cart page based on stock_changed
    # Notify if there are changes in cart
    # if stock_changed:
    #     messages.add_message(request, messages.INFO, 'Stock has fewer amount than some of the products in your cart! Please refresh the page to update the changes!')

    total_price = 0
    for cart_data in cart:
        total_price += cart_data.get('price') * cart_data.get('quantity')
    return render(request, 'cart.html', {'cart': cart, 'total': total_price, 'changed': stock_changed})


def orders(request):
    orders_list = OrderDJ.objects.filter(user=request.user.username)

    return render(request, 'order.html', {'orders': orders_list})


def checkout(request):
    # delete old messages
    storage = messages.get_messages(request)
    storage.used = True

    cart = Cart.objects.filter(user=request.user.username).values('product_id', 'product_name', 'product_image', 'price', 'user').annotate(quantity=Sum('quantity'))
    products = Product.objects.all()
    total_price = 0
    for cart_data in cart:
        total_price += cart_data.get('price') * cart_data.get('quantity')

    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
    else:
        name = ''
        address = ''
        phone = ''

    if name and address:
        # Create an order
        order = OrderDJ(user=request.user.username, customer_name=name, address=address, phone_number=phone, total_price=total_price)

        # If success, create orderdetail
        if order:
            order.save()
            messages.add_message(request, messages.INFO, 'Order accepted! Wait for your delivery!')

            for item in cart:
                # Add to order table
                order_detail = OrderDetailsDJ(order_id=order, product_id=item.get('product_id'), user=item.get('user'), quantity=item.get('quantity'), price=item.get('price'))
                order_detail.save()
                # Decrease quantity in stock
                product = products.get(product_id=item.get('product_id'))
                stock_left = product.quantity_in_stock - item.get('quantity')
                product.quantity_in_stock = stock_left
                product.save(update_fields=['quantity_in_stock'])

            # Empty your cart
            Cart.objects.filter(user=request.user.username).delete()
            return redirect('/')
        messages.add_message(request, messages.INFO, 'Oops!')

    return render(request, 'checkout.html', {'cart': cart, 'total': total_price})


def delete_cart(request, pid):
    Cart.objects.filter(user=request.user.username, product_id=pid).delete()
    return redirect('/products/cart')
