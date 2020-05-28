from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from products.models import Product, OrderDJ, OrderDetailsDJ

# Create your views here.


### Admin's product functions ###
def product(request):
    if request.user.is_superuser:
        pds = Product.objects.all()
        return render(request, 'admin_product.html', {'products': pds})
    return HttpResponse("You don't have permission to view this page")


def product_change(request, pid):
    if request.user.is_superuser:
        url = "/admin/products/accept_change/" + pid
        product = Product.objects.get(product_id=pid)
        return render(request, 'product_change.html', {'product': product, 'url': url})
    return HttpResponse("You don't have permission to view this page")


def product_add(request):
    if request.user.is_superuser:
        url = "/admin/products/accept_add/"
        return render(request, 'product_change.html', {'url': url})
    return HttpResponse("You don't have permission to view this page")


def product_accept_change(request, pid):
    if request.user.is_superuser:
        product = Product.objects.get(product_id=pid)
        if request.method == 'POST':
            product_id = request.POST['product_id']
            product_name = request.POST['product_name']
            product_image = request.POST['product_image']
            company = request.POST['company']
            product_description = request.POST['product_description']
            quantity = request.POST['quantity']
            price = request.POST['price']

            # Update any fields that's different
            if product_id != product.product_id:
                product.product_id = product_id
                product.save(update_fields=["product_id"])

            if product_name != product.product_name:
                product.product_name = product_name
                product.save(update_fields=["product_name"])

            if product_image != product.product_image:
                product.product_image = product_image
                product.save(update_fields=["product_image"])

            if company != product.company:
                product.company = company
                product.save(update_fields=["company"])

            if product_description != product.product_description:
                product.product_description = product_description
                product.save(update_fields=["product_description"])

            if quantity != product.quantity_in_stock:
                product.quantity_in_stock = quantity
                product.save(update_fields=["quantity_in_stock"])

            if price != product.sell_price:
                product.sell_price = price
                product.save(update_fields=["sell_price"])

        return redirect('/admin/products')
    return HttpResponse("You don't have permission to view this page")


def product_accept_add(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            product_id = request.POST['product_id']
            product_name = request.POST['product_name']
            product_image = request.POST['product_image']
            company = request.POST['company']
            product_description = request.POST['product_description']
            quantity = request.POST['quantity']
            price = request.POST['price']

            product = Product(product_id=product_id, product_name=product_name, product_image=product_image, company=company, product_description=product_description, quantity_in_stock=quantity, sell_price=price)
            product.save()

            return redirect('/admin/products')
        else:
            messages.add_message(request, messages.INFO, 'Error! Please refill the form to add a product')
            return redirect('/admin/products/add')
    return HttpResponse("You don't have permission to view this page")


### Admin's order functions ###
def order(request):
    if request.user.is_superuser:
        orders_list = OrderDJ.objects.all()

        return render(request, 'admin_order.html', {'orders': orders_list})
    return HttpResponse("You don't have permission to view this page")


def status_change(request, oid):
    if request.user.is_superuser:
        order = OrderDJ.objects.get(order_id=oid)

        if order.shipped is False:
            order.shipped = True
        else:
            order.shipped = False

        order.save(update_fields=["shipped"])
        return redirect('/products/orders')
    return HttpResponse("You don't have permission to view this page")


def details(request, oid):
    if request.user.is_superuser:
        order = OrderDJ.objects.get(order_id=oid)
        order_details = OrderDetailsDJ.objects.filter(order_id=oid).select_related('pd')

        return render(request, 'admin_orderdetails.html', {'id': oid, 'shipped': order.shipped, 'details': order_details, 'total': order.total_price})
    return HttpResponse("You don't have permission to view this page")
