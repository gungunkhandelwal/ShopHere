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
    digital = models.BooleanField(default=False, null=True, blank=True)


    def __str__(self):
        return self.prod_name
    
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)
    transaction_id=models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping=False
        orderitems=self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital ==False:
                shipping=True
            return shipping
    
    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total
    
class OrderItem(models.Model):
    product=models.ForeignKey(Product_details,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total=self.product.price*self.quantity
        return total
    

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
    
class ContactUs(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=70, default="")
    desc = models.TextField()


    def __str__(self):
        return self.name