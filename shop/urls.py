from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('cart/',views.cart,name='Cart'),
    path('checkout/',views.checkout,name='Checkout'),
    path("products/<int:myid>", views.prodView, name="ProdView"),
    path('contact/',views.contact,name='ContactUs'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'),
    path('update_user/',views.update_user,name='update_user'),
    path('update_password/',views.update_password,name='update_password'),


    path('update_item/',views.updateItem,name='update_item'),
    path('process_order/',views.processOrder,name='process_order'),
]