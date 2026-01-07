from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# class Adminlogin(models.Model):
#     email=models.EmailField(unique=True)
#     password=models.TextField()

class perfume(models.Model):
    img=models.FileField(upload_to='uploads/')
    name=models.TextField()
    price=models.IntegerField()

class PerfumeDetail(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unisex'),
    )

    perfume = models.ForeignKey(
        perfume,
        on_delete=models.CASCADE,
        related_name='details',null=True, blank=True
    )
    about = models.TextField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    stock=models.IntegerField(default=0)
    
class new(models.Model):
    name=models.TextField()
    img=models.FileField(upload_to='uploads/')

class Cart(models.Model):
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='details',null=True, blank=True)
    img=models.FileField(upload_to='uploads/')
    name=models.TextField()
    price=models.IntegerField()
    product_id=models.IntegerField(null=True)


class Order(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    full_name    = models.CharField(max_length=255)
    email        = models.EmailField()
    gender       = models.TextField(max_length=50, blank=True, null=True)    # if you really need gender
    state        = models.CharField(max_length=100)
    district     = models.CharField(max_length=100)
    address      = models.TextField()
    pincode      = models.CharField(max_length=20)
    landmark     = models.CharField(max_length=255, blank=True, null=True)

    order_date   = models.TextField()
    delivered_date = models.TextField(blank=True, null=True)
    totalprice=models.IntegerField(blank=True,null=True)
    product_id=models.IntegerField()
    product_name=models.TextField()
    quantity=models.IntegerField()
    img=models.FileField()

class Wish(models.Model):
    users=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users',null=True, blank=True)
    perfume = models.ForeignKey(perfume, on_delete=models.CASCADE,related_name='perfume',null=True,blank=True)
    notified = models.BooleanField(default=False)

    




    




