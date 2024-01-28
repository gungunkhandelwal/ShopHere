import json
from .models import *

def cookieCart(request):

    try:
       cart=json.loads(request.COOKIES['cart'])
    except:
        cart={}
    items=[]
    order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
    cartItems=order['get_cart_items']

    for i in cart:

            try:
                cartItems +=cart[i]['quantity']
                product=Product_details.objects.get(id=i)
                total=(product.price * cart[i]['quantity'])

                order['get_cart_total'] +=total
                order['get_cart_items'] += cart[i]['quantity']

                item={
                    'product':{
                    'id':product.prod_id,
                    'name':product.prod_name,
                    'price':product.price,
                    'image':product.image
                },
                'quantity':cart[i]['quantity'],
                'get_total':total,
                }

                items.append(item)

                if product.digital ==False:
                    order['shipping'] =True
            except:
                 pass
    return {'cartItems':cartItems,'order':order,'items':items}

def cartData(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            customer = None

        if customer:
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cart_items = order.get_cart_items
        else:
            # Handle the case where the user does not have a related Customer object
            # (perhaps redirect them to a profile setup page or something similar)
            cart_items, order, items = None, None, None
    else:
        cookie_data = cookieCart(request)
        cart_items = cookie_data['cartItems']
        order = cookie_data['order']
        items = cookie_data['items']

    return {'cartItems': cart_items, 'order': order, 'items': items}
