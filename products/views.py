from django.shortcuts import render
from .models import Products

# Create your views here.


def home(request):
    pds = Products.objects.all()
    return render(request, 'product.html', {'products': pds})
