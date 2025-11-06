from django.db import models

# Create your models here.
class Adminlogin(models.Model):
    email=models.EmailField(unique=True)
    password=models.TextField()
class Perfumes(models.Model):
    img=models.FileField(upload_to='uploads/')
    name=models.TextField()
    price=models.IntegerField()
