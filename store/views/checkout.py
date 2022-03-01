from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.views import View
import random
from Eshop import settings
from store.models.product import Product
from store.models.orders import Order
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import render_to_string, get_template

@login_required(login_url='login')
def checkout(request):
    address = request.POST.get('address')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    cart = request.session.get('cart')
    customer = request.session.get('customer')
    products = Product.get_products_by_id(list(cart.keys()))
    print(address, phone, customer, cart, products)
    ordering_code= ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567893456789') for _ in range(6)])

    for product in products:
        print(cart.get(str(product.id)))
        order = Order(customer=User(id=customer),
                      product=product,
                      price=product.price,
                      address=address,
                      phone=phone,
                      email=email,
                      ordering_code=ordering_code,
                      quantity=cart.get(str(product.id)))
        order.save()
    
    
    ctx = {
        'products': products,
    }

    message = get_template('cart.html').render(context(ctx))
    if address:
        send_mail(
                'That’s your subject',
                message,
                settings.EMAIL_HOST_USER,
                [f'{email}'],
                fail_silently = False,
            )
    messages.success(request, f'Dear Customer Your Order as been Recived  Successfully, Will be delivered To {address} within 24 hours')
    request.session['cart'] = {}
    return redirect('store')
