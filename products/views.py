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


def product_search(request):
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
    return render(request, 'product_details.html', {'product': product, 'quantity': quantity})


def cart_add(request, pid):
    if request.user.is_superuser:
        return HttpResponse("Invalid")
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

    in_cart = Cart.objects.filter(user=request.user.username, product_id__pk=pid)
    cart_quantity = 0
    if in_cart:
        cart_quantity = in_cart.get(product_id__pk=pid).quantity

    if quantity != 0 and user != "none":
        if int(quantity) + cart_quantity > product_stock:
            messages.add_message(request, messages.INFO, "Heyyyy! You know we do not have that many right?")
        else:
            messages.add_message(request, messages.INFO, 'You have added a product to your cart!')
            product_temp = Cart.objects.filter(user=request.user.username, product_id__pk=pid)
            if product_temp:
                pd_temp = product_temp.get(product_id__pk=pid)
                pd_temp.quantity = int(quantity) + cart_quantity
                pd_temp.save(update_fields=['quantity'])
            else:
                print('Product not found. Creating new.')
                product_new = Cart(product_id=Product.objects.get(product_id=pid), quantity=quantity, user=user)
                product_new.save()
    else:
        messages.add_message(request, messages.INFO, 'Oops!')

    return redirect('/products')


def cart_get(request):
    if request.user.is_superuser:
        return HttpResponse("Invalid")
    cart = Cart.objects.filter(user=request.user.username).select_related('product_id')
    stock_changed = False
    total_price = 0
    for item in cart:
        in_stock = item.product_id.quantity_in_stock
        # If empty stock, remove entry from cart
        if in_stock == 0:
            Cart.objects.filter(user=request.user.username, product_id=item.product_id).delete()
            stock_changed = True
        # Else, change the quantity of that entry in cart
        elif item.quantity > in_stock:
            Cart.objects.filter(user=request.user.username, product_id=item.product_id).update(quantity=in_stock)
            stock_changed = True

        total_price += item.product_id.sell_price * item.quantity

    return render(request, 'cart.html', {'cart': cart, 'changed': stock_changed, 'total': total_price})


def orders_get(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            orders_list = Orders.objects.order_by('-order_id')
        else:
            orders_list = Orders.objects.filter(user=request.user.username).order_by('-order_id')
        return render(request, 'order.html', {'orders': orders_list})
    return HttpResponse("You don't have permission to view this page")


def cart_checkout(request):
    if request.user.is_superuser:
        return HttpResponse("Invalid")
    # delete old messages
    storage = messages.get_messages(request)
    storage.used = True

    cart = Cart.objects.filter(user=request.user.username).select_related('product_id')
    total_price = 0
    for item in cart:
        total_price += item.product_id.sell_price * item.quantity

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
                order_detail = OrderDetails(order_id=order, user=item.user, quantity=item.quantity, product_id=Product.objects.get(product_id=item.product_id.product_id))
                order_detail.save()
                # Decrease quantity in stock
                # product = products.get(product_id=item.product_id.product_id)
                item.product_id.quantity_in_stock -= item.quantity
                item.product_id.save(update_fields=['quantity_in_stock'])

            # Empty your cart
            Cart.objects.filter(user=request.user.username).delete()
            return redirect('/')
        messages.add_message(request, messages.INFO, 'Oops!')

    return render(request, 'checkout.html', {'cart': cart, 'total': total_price})


def cart_delete(request, pid):
    if request.user.is_superuser:
        return HttpResponse("Invalid")
    Cart.objects.filter(product_id__pk=pid).delete()
    return redirect('/products/cart')


def order_cancel(request, oid):
    if request.user.is_superuser:
        return HttpResponse("Invalid")
    order = Orders.objects.get(order_id=oid)
    order.status = 'Canceled'
    order.save(update_fields=['status'])
    return redirect('/products/orders')


def order_details(request, oid):
    if request.user.is_superuser:
        return redirect('/admin/orders')
    order = Orders.objects.get(order_id=oid)
    details = OrderDetails.objects.filter(order_id=oid).select_related('product_id')

    return render(request, 'order_details.html', {'id': oid, 'status': order.status, 'details': details, 'total': order.total_price})
