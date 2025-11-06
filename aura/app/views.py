from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .models import *



# Create your views here.
def home(request):
    data=Perfumes.objects.all()

    return render(request ,'home.html',{'data':data})


def adminlogin(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        print(email,password)
        user=User.objects.get(email=email)
        if user is not None and user.check_password(password):
            return redirect(adddetails)
    return render(request, 'admin.html')


def adddetails(request):
    if not request.user.is_authenticated:   
        return redirect(adminlogin)
    else:
        if request.method=='POST':
            file1=request.FILES.get('file1')
            name=request.POST['name']
            price=request.POST['price']
            data=Perfumes.objects.create(img=file1,name=name,price=price)
            data.save()
        return render(request,'add.html')
    
    