from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Product, Order, OrderItem
from django.views.generic import DetailView
# Create your views here.

def index(request):
    products = Product.objects.all()
    return render(request, 'main/index.html', {'products': products})

def about(request):
    return render(request, 'main/about.html')

def cart(request):
    return render(request, 'main/cart.html')

def Product_details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    context = {
        'product': product,
    }
    return render(request, 'main/detail_view.html', context)

def add_to_cart_logic(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    product_id_str = str(product.id)
    
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 0
    else:
        cart[product_id_str] = {
            'slug': product.slug,
            'price': str(product.price),
            'quantity': 1,
            'title': product.title,
        }
        if product.images.first():
            cart[product_id_str]['image'] = product.images.first().image.url
        else:
            cart[product_id_str]['image'] = ''

    request.session['cart'] = cart
    request.session.modified = True

def cart_add(request, product_id):
    add_to_cart_logic(request, product_id)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def cart_add_and_buy(request, product_id):
    add_to_cart_logic(request, product_id)
    return redirect('cart')

def cart_detail(request):
    
    cart = request.session.get('cart', {})
    all_price = 0
    
    for i in cart.values():
        i['total_price'] = float(i['price']) * i['quantity']
        all_price += i['total_price']
        
    context = {
        'cart': cart,
        'all_price': all_price,
    }
    return render(request, 'main/cart.html', context)

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
        
    return redirect('cart')

def cart_decrement(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)  
    
    if product_id_str in cart:
        
        if cart[product_id_str]['quantity'] > 1:
            cart[product_id_str]['quantity'] -= 1
        else:
            
            del cart[product_id_str]
            
        request.session['cart'] = cart
        request.session.modified = True
        
    return redirect(request.META.get('HTTP_REFERER', 'cart'))

def cart_increment(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1  
        
    request.session['cart'] = cart
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def create_order(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        phone = request.POST.get('phone')
        delivery_service = request.POST.get('delivery_service')
        city = request.POST.get('city')
        department = request.POST.get('department')

        cart = request.session.get('cart', {})
        if not cart:
            return redirect('cart')

        order = Order.objects.create(
            first_name=first_name,
            phone=phone,
            delivery_service=delivery_service,
            city=city,
            department=department
        )

        for product_id, item in cart.items():
            OrderItem.objects.create(
                order=order,
                product_title=item['title'],
                price=item['price'],
                quantity=item['quantity']
            )

        request.session['cart'] = {}
        request.session.modified = True

        payment_type = request.POST.get('payment_type')

        if payment_type == 'online':

            return redirect('order_success')
        else:
            return redirect('order_success')
    return redirect('cart')

def checkout_view(request):
    return render(request, 'main/checkout.html')

def order_success_view(request):
    return render(request, 'main/order_success.html')