from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager


class Address(models.Model):
    name=models.CharField(max_length=90)
    email=models.CharField(max_length=111)
    address=models.CharField(max_length=111)
    city=models.CharField(max_length=111)
    state=models.CharField(max_length=111)
    zip_code=models.CharField(max_length=111)
    phone=models.CharField(max_length=111, default='')

class CustomUser(AbstractUser):
    """User model."""

    username = None
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(_('email address'), unique=True)
    address = models.ManyToManyField(Address)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = UserManager()
    def __str__(self):
        return self.email



class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.category



class Product(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=50)
    prod_img = models.ImageField(upload_to='static/images', default="")
    prod_desc = models.CharField(max_length=300)
    prod_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    prod_price = models.IntegerField(default=0)
    prod_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.prod_name

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)

    def __str__(self):
        return self.name

status_choices = (
    ('O', 'Ordered'),
    ('S', 'Shipped'),
    ('OTW', 'On the way'),
    ('D', 'Delivered')
)

    
class OrderProd(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.prod_name}"

    def get_total_prod_price(self):
        return self.quantity * self.product.prod_price




class Orders(models.Model):
    order_id= models.AutoField(primary_key=True)
    products= models.ManyToManyField(OrderProd)
    total_price= models.FloatField()
    user= models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    payment_mode=models.CharField(max_length=111)
    date=models.DateTimeField(_("Date"),  auto_now_add=True)
    status=models.CharField(choices=status_choices,max_length=3,default='O',null=True)
    def __str__(self):
        return self.user.email

    def get_total(self):
        total = 0
        for product in self.products.all():
            total += product.get_total_prod_price()
        return total
