from django.http import JsonResponse
from django.shortcuts import render
from .models import *
import json
import datetime
from .utils import cookie_cart, cart_data, guest_order


# Create your views here.
def index(request):
    return render(request, 'gardenApp/index.html')


def contact(request):
    return render(request, 'gardenApp/contact.html')


def about_us(request):
    return render(request, 'gardenApp/about_us.html')


def shop(request):
    return render(request, 'gardenApp/shop.html')


def checkout(request):
    data = cart_data(request)
    cartItem = data['cartItem']
    order = data['order']
    items = data['items']
    context = {'order': order, 'items': items, 'cartItem': cartItem}
    return render(request, 'gardenApp/checkout.html', context)


def store(request):
    data = cart_data(request)
    cartItem = data['cartItem']
    products = Product.objects.all()
    content = {'products': products, 'cartItem': cartItem}
    return render(request, 'gardenApp/store.html', content)


def cart(request):
    data = cart_data(request)
    cartItem = data['cartItem']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartItem': cartItem}
    return render(request, 'gardenApp/cart.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

        order.save()
    else:
        customer, order = guest_order(request, data)

        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True

        order.save()

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    return JsonResponse('Payment submitted..', safe=False)
