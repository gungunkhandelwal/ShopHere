from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
import json
import datetime
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm,UpdateUserForm,ChangePassword
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
    data=cartData(request)  #Request data from cartData function
    
    cartItems=data['cartItems'] #Get number of item present in cart
    
    product=Product_details.objects.filter(id=myid)
    #Fetch the product using the id
    return render(request, "prodView.html",{'products':product[0],'cartItems':cartItems})

def contact(request):
    data=cartData(request)  #Request data from cartData function
    
    cartItems=data['cartItems'] #Get number of item present in cart
    if request.method=="POST":
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        desc=request.POST.get('desc', '')
        contact = ContactUs(name=name, email=email,desc=desc)
        contact.save()
    return render(request,'contact.html',{'cartItems':cartItems})

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

# User authentication

def login_user(request):
    data=cartData(request)  #Request data from cartData function
    
    cartItems=data['cartItems'] #Get number of item present in cart
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,('You have been logged In!!'))
            return redirect('index')
        else:
            print('Error')
            return render(request,'login.html',{'cartItems':cartItems})
    else:
        return render(request,'login.html',{'cartItems':cartItems})

def logout_user(request):
    logout(request)
    messages.success(request,('You have been logged out !'))
    return redirect('index')

def register_user(request):
    form=SignUpForm()
    if request.method =='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            # log in user
            user=authenticate(request,username=username,password=password)
            login(request,user)
            messages.success(request,('You have Registered succesfully!! Welcome to ShopHere !! Please login to Explore !'))
            return redirect('index')
        else:
            messages.success(request,('There is an error,Try Again..'))
            return redirect('register')
    else:
        return render(request,'register.html',{'form':form})
    

def update_user(request):
    data=cartData(request)  #Request data from cartData function
    
    cartItems=data['cartItems'] #Get number of item present in cart
    if request.user.is_authenticated:
        current_users=User.objects.get(id=request.user.id)
        user_form=UpdateUserForm(request.POST or None,instance=current_users)

        if user_form.is_valid():
            user_form.save()
            login(request,current_users)
            messages.success(request,"User has been Uploaded !!")
            return redirect('index')
        return render(request,'update_user.html',{'user_form':user_form,'cartItems':cartItems})
    else:
        messages.success(request,"You must belogged in !!")
        return redirect('index')

def update_password(request):
    data=cartData(request)  #Request data from cartData function
    
    cartItems=data['cartItems'] #Get number of item present in cart
    if request.user.is_authenticated:
        current_user=request.user
        if request.method =='POST':
            form=ChangePassword(current_user,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"You have been Change Password Successfully!! Please Login In again ")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
        else:
            form=ChangePassword(current_user)
            return render(request,'update_password.html',{'form':form,'cartItems':cartItems})
    else:
        messages.success(request,"You have been login in")
        return redirect('index')
    return render(request,'update_password.html',{'form':form,'cartItems':cartItems})