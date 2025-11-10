from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .models import *
from django.contrib.auth import authenticate, login
User = get_user_model()





# Create your views here.
def home(request):
    data = perfume.objects.all().prefetch_related('details')
   

    return render(request ,'home.html',{'data':data})


def adminlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            print(user.email)
        except User.DoesNotExist:
            user = None

        if user is not None and user.check_password(password):
            login(request,user)
            return redirect(adddetails)
           

    return render(request, 'admin.html')



def adddetails(request):
    if not request.user.is_authenticated:   
        return redirect(adminlogin)
    else:
        if request.method=='POST':
            file1=request.FILES.get('image')
            name=request.POST['name']
            price=request.POST['price']
            about=request.POST['about']
            gender=request.POST['gender']
            stock=request.POST['stock']


           
            data=perfume.objects.create(img=file1,name=name,price=price) 
        
            PerfumeDetail.objects.create(perfume=data ,about=about,gender=gender,stock=stock)
            data.save()
        return render(request,'adds.html')
    

def catalogs(request):
        return render(request,'catalog.html')

def viewall(request,id):
    data=perfume.objects.filter(id=id)
    
    d=PerfumeDetail.objects.filter(perfume_id=id)
    print(d)
    return render(request,'view.html',{'data':data,'d':d})
    