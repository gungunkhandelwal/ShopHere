from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    Cust_name=models.CharField(max_length=100,default=" ")
    email=models.EmailField(max_length=200,default="abc@gmail.com")

    def __str__(self):
        return self.Cust_name

class Product_details(models.Model):
    prod_id=models.AutoField
    prod_name=models.CharField(max_length=30)
    prod_desc=models.TextField()
    image = models.ImageField(upload_to='product/images', default="")
    price = models.IntegerField(default=0)
    pub_date=models.DateField(auto_now_add=True)
    category=models.CharField(max_length=50,default="Sale")

    def __str__(self):
        return self.prod_name
    
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)
    transaction_id=models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.id)
    
class OrderItem(models.Model):
    product=models.ForeignKey(Product_details,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    

class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=200,null=False)
    state=models.CharField(max_length=200,null=False)
    zipcode=models.CharField(max_length=200,null=False)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address