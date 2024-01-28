from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
import datetime
from django.views.decorators.csrf import csrf_exempt


from .utilis import cookieCart ,cartData

def index(request):
    data=cartData(request)  #Request data from cartData function
    
    cartItems=data['cartItems'] #Get number of item present in cart
    
    #Fetching data from models
    products=Product_details.objects.all() 
    details={'products':products,'cartItems':cartItems} 
    return render(request,'store.html',details)

def cart(request):
    data=cartData(request)
    
    cartItems=data['cartItems']
    order=data['order'] #Total number of order from Order model
    items=data['items'] # Get items in the cart present
    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'cart.html',context)

def checkout(request):
    data=cartData(request)
    
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']

    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'checkout.html',context)

def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']

    customer=request.user.customer
    product=Product_details.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)


    orderItem,created= OrderItem.objects.get_or_create(order=order,product=product)
    if action =='add':
        orderItem.quantity=(orderItem.quantity+1)
    
    elif action == 'remove':
        orderItem.quantity=(orderItem.quantity -1)
    orderItem.save()
    

    if orderItem.quantity <=0:
        orderItem.delete()
    return JsonResponse('Item was added',safe=False)

def prodView(request, myid):
    product=Product_details.objects.filter(id=myid)
    #Fetch the product using the id
    return render(request, "prodView.html",{'products':product[0]})

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        desc=request.POST.get('desc', '')
        contact = ContactUs(name=name, email=email,desc=desc)
        contact.save()
    return render(request,'contact.html')

@csrf_exempt
def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        total=float(data['form']['total'])
        order.transaction_id=transaction_id

        if total == order.get_cart_total:
            order.complete=True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
                )
    else:
        print('User is not logged in ..')
    return JsonResponse('Payment complete',safe=False)
