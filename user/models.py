from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    image = models.ImageField(default="profilepic.jpeg",upload_to='profile_pictures')

    def __str__(self):
        return self.user.username


class Wishlist(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)


class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    city = models.CharField(max_length=200,default='city')
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    address = models.CharField(max_length=200,default='address')
    address2 = models.CharField(max_length=200,default='address2')


