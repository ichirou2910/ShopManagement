"""Import models"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, Q
from django.http import HttpResponse
from .models import Product, Cart, Orders, OrderDetails

# Create your views here.


def home(request):
    """ Render product page """
    pds = Product.objects.all().order_by('product_id')
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
    if request.user.is_superuser:
        return redirect('/admin/orders')
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
    product_stock = product_get.quantity_in_stock

    in_cart = Cart.objects.filter(user=request.user.username, product_id=pid)
    cart_quantity = 0
    if in_cart:
        cart_quantity = in_cart.get(product_id=pid).quantity
        print(cart_quantity)

    if quantity != 0 and user != "none":
        if int(quantity) + cart_quantity > product_stock:
            messages.add_message(request, messages.INFO, "Heyyyy! You know we do not have that many right?")
        else:
            messages.add_message(request, messages.INFO, 'You have added a product to your cart!')
            product_temp = Cart.objects.filter(user=request.user.username, product_id=pid)
            if product_temp:
                pd = product_temp.get(product_id=pid)
                pd.quantity = int(quantity) + cart_quantity
                pd.save(update_fields=['quantity'])
            else:
                print('Product not found. Creating new.')
                product_new = Cart(product_id=pid, pd=Product.objects.get(product_id=pid), quantity=quantity, user=user)
                product_new.save()
    else:
        messages.add_message(request, messages.INFO, 'Oops!')

    return redirect('/products')


def cart_get(request):
    if request.user.is_superuser:
        return redirect('/admin/orders')
    cart = Cart.objects.filter(user=request.user.username).select_related('pd')
    stock_changed = False
    total_price = 0
    for item in cart:
        in_stock = Product.objects.get(product_id=item.product_id).quantity_in_stock
        # If empty stock, remove entry from cart
        if in_stock == 0:
            Cart.objects.filter(user=request.user.username, product_id=item.product_id).delete()
            stock_changed = True
        # Else, change the quantity of that entry in cart
        elif item.quantity > in_stock:
            Cart.objects.filter(user=request.user.username, product_id=item.product_id).update(quantity=in_stock)
            stock_changed = True

        total_price += Product.objects.get(product_id=item.product_id).sell_price * item.quantity

    return render(request, 'cart.html', {'cart': cart, 'changed': stock_changed, 'total': total_price})


def orders(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            orders_list = Orders.objects.order_by('order_id')
        else:
            orders_list = Orders.objects.filter(user=request.user.username).order_by('order_id')
        return render(request, 'order.html', {'orders': orders_list})
    return HttpResponse("You don't have permission to view this page")


def checkout(request):
    if request.user.is_superuser:
        return redirect('/admin/orders')
    # delete old messages
    storage = messages.get_messages(request)
    storage.used = True

    cart = Cart.objects.filter(user=request.user.username).select_related('pd')
    products = Product.objects.all()
    total_price = 0
    for item in cart:
        total_price += item.pd.sell_price * item.quantity

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
        order = Orders(user=request.user.username, customer_name=name, address=address, phone_number=phone, total_price=total_price)

        # If success, create orderdetail
        if order:
            order.save()
            messages.add_message(request, messages.INFO, 'Orders accepted! Wait for your delivery!')

            for item in cart:
                # Add to order table
                order_detail = OrderDetails(order_id=order, product_id=item.product_id, user=item.user, quantity=item.quantity, pd=Product.objects.get(product_id=item.product_id))
                order_detail.save()
                # Decrease quantity in stock
                product = products.get(product_id=item.product_id)
                product.quantity_in_stock = product.quantity_in_stock - item.quantity
                product.save(update_fields=['quantity_in_stock'])

            # Empty your cart
            Cart.objects.filter(user=request.user.username).delete()
            return redirect('/')
        messages.add_message(request, messages.INFO, 'Oops!')

    return render(request, 'checkout.html', {'cart': cart, 'total': total_price})


def delete_cart(request, pid):
    if request.user.is_superuser:
        return redirect('/admin/orders')
    Cart.objects.filter(user=request.user.username, product_id=pid).delete()
    return redirect('/products/cart')
