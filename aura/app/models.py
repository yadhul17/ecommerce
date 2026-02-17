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
    PAYMENT_CHOICES = [
        ("COD", "Cash On Delivery"),
        ("CARD", "Card Payment"),
        ("UPI", "UPI Payment"),
        ("WALLET", "Wallet"),
    ]

    ORDER_STATUS = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    user             = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    full_name        = models.CharField(max_length=255)
    email            = models.EmailField()
    gender           = models.TextField(max_length=50, blank=True, null=True)
    state            = models.CharField(max_length=100)
    district         = models.CharField(max_length=100)
    address          = models.TextField()
    pincode          = models.CharField(max_length=20)
    landmark         = models.CharField(max_length=255, blank=True, null=True)

    order_date       = models.TextField()
    delivered_date   = models.TextField(blank=True, null=True)
    totalprice       = models.IntegerField(blank=True, null=True)
    product_id       = models.IntegerField()
    product_name     = models.TextField()
    quantity         = models.IntegerField()
    img              = models.FileField()

    payment_mode     = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="COD",
    )

    # 🆕 Order status field
    status           = models.CharField(
        max_length=15,
        choices=ORDER_STATUS,
        default="Pending"
    )

    # 🆕 (Optional) Refund fields
    refund_id        = models.CharField(max_length=100, blank=True, null=True)
    refund_status    = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product_name} ({self.status})"

    def __str__(self):
        return f"Order #{self.id} by {self.full_name}"


class Payment(models.Model):
    # Status choices for better tracking
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    )

    # Note: Using 'users' because your previous errors showed 
    # your project uses 'users' as the field name for the User relation.
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Linked to your Order model
    orders = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Razorpay Specific IDs
    provider_order_id = models.CharField(max_length=100, unique=True)
    payment_id = models.CharField(max_length=100, blank=True)
    signature_id = models.CharField(max_length=128, blank=True)
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='PENDING'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.provider_order_id} - {self.status}"

class Wish(models.Model):
    users=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users',null=True, blank=True)
    perfume = models.ForeignKey(perfume, on_delete=models.CASCADE,related_name='perfume',null=True,blank=True)
    notified = models.BooleanField(default=False)


class Profile(models.Model):
    # Link to the built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name=models.TextField(max_length=25,null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    
    # Metadata
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    




    




