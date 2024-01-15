from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('cart/',views.cart,name='Cart'),
    path('checkout/',views.checkout,name='Checkout'),
]