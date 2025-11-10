from django.db import models

# Create your models here.
class Adminlogin(models.Model):
    email=models.EmailField(unique=True)
    password=models.TextField()

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




