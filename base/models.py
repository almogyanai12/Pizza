from django.db import models
from django.contrib.auth.models import User # watch out, always create a custom User model with
# the following before first migrating the project

class CustomUser(AbstractUser): # import this from django
    # even if you have nothing change this and add in your settings model the following line:
    # AUTH_USER_MODEL = 'base.CustomUser'
    pass
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True) 
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(max_length=200, null=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property 
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Topping(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True) # can be auto field - so you won't have to deal with this
    pizza = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property # no need for propery, better way: read about custom manager, https://www.youtube.com/watch?v=YGwSNkdwAEs&t=674s  -see all django con, amazing hacks there
    def get_cart_total(self):
        orderitems = self.orderitem_set.all() # where is the orederitem field, i'm confused, a set suggests a foreign key(?) ?
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model): # I don't understand why you need two order models, use one.
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0, null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    toppings = models.ManyToManyField(Topping)


    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True,null=True) # do you understand on_delete? , almost in any case you'll want models.CASCADE
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    city = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.address
