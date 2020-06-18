import json
from .models import *


def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print("Cart:", cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItem = order['get_cart_items']

    for i in cart:
        try:
            cartItem += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'id': product.id,
                'product':
                    {'id': product.id, 'name': product.name, 'price': product.price,
                     'imageURL': product.imageURL},
                'quantity': cart[i]['quantity'],
                'digital': product.digital,
                'get_total': total,
            }
            items.append(item)

            if not product.digital:
                order['shipping'] = True
        except:
            pass

    return {'cartItem': cartItem, 'order': order, 'items': items}


def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        cookieData = cookie_cart(request)
        cartItem = cookieData['cartItem']
        order = cookieData['order']
        items = cookieData['items']
    context = {'order': order, 'items': items, 'cartItem': cartItem}
    return context


def guest_order(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookie_data = cookie_cart(request)
    item = cookie_data['item']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )
    for items in item:
        product = Product.objects.get(id=item['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )
    return customer, order
