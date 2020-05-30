from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from products.models import Product, Orders, OrderDetails

# Create your views here.


# Admin's product functions
def product_change(request, pid):
    if request.user.is_superuser:
        url = "/admin/products/accept_change/" + pid
        product = Product.objects.get(product_id=pid)
        return render(request, 'product_change.html', {'product': product, 'url': url})
    return HttpResponse("You don't have permission to view this page")


def product_add(request):
    if request.user.is_superuser:
        url = "/admin/products/accept_add/"
        return render(request, 'product_add.html', {'url': url})
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

        return redirect('/products')
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

            return redirect('/products')
        messages.add_message(request, messages.INFO, 'Error! Please refill the form to add a product')
        return redirect('/admin/products/add')
    return HttpResponse("You don't have permission to view this page")


def product_delete(request, pid):
    if request.user.is_superuser:
        Product.objects.get(product_id=pid).delete()
        return redirect('/products')
    return HttpResponse("You don't have permission to view this page")


# Admin's order functions
def order_status_change(request, oid):
    if request.user.is_superuser:
        order = Orders.objects.get(order_id=oid)

        if order.status == 'Pending':
            order.status = 'Confirmed'

        order.save(update_fields=["status"])
        return redirect('/products/orders')
    return HttpResponse("You don't have permission to view this page")


def order_filter(request):
    if request.user.is_superuser:
        order = Orders.objects.all()
        if 'status' in request.GET:
            status = request.GET["status"]
            if status == 'confirmed':
                order = order.filter(status="Confirmed")
            elif status == 'pending':
                order = order.filter(status="Pending")
            elif status == 'cancelled':
                order = order.filter(status="Canceled")

        return render(request, 'order.html', {'orders': order})
    return HttpResponse("You don't have permission to view this page")


def order_details(request, oid):
    order = Orders.objects.get(order_id=oid)
    details = OrderDetails.objects.filter(order_id=oid).select_related('product_id')

    return render(request, 'order_details.html', {'id': oid, 'status': order.status, 'details': details, 'total': order.total_price})
