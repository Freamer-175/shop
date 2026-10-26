from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
# Create your views here.

def index(request):
    products = Product.objects.all()
    return render(request, 'main/index.html', {'products': products})

def about(request):
    return render(request, 'main/about.html')

def cart(request):
    return render(request, 'main/cart.html')