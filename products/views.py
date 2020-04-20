"""Import models"""
from django.shortcuts import render
from .models import Product

# Create your views here.


def home(request):
    """ Render product page """
    pds = Product.objects.all()
    return render(request, 'product.html', {'products': pds})

def product_details(request, pid):
    product = Product.objects.get(product_id=pid)
    return render(request, 'details.html', {'product': product})
