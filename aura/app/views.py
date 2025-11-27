from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .models import *
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.shortcuts import get_object_or_404
from datetime import date, timedelta
from django.db.models import F
from django.core.mail import send_mail

User = get_user_model()





# Create your views here.
def home(request):
    data = perfume.objects.all().prefetch_related('details')[:4]
    d=new.objects.all()[:4]
    user = request.user
    print(user)
    if not user.is_authenticated:
        return redirect(login_view)  
    



   

    return render(request ,'home.html',{'data':data,'d':d})


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
def adddetail(request):
    if not request.user.is_authenticated:   
        return redirect(adminlogin)
    else:
        if request.method=='POST':
            file1=request.FILES.get('image')
            name=request.POST['name']
            print(file1,name)
            d=new.objects.create(img=file1,name=name) 
        
           
            d.save()
       
             
        
        return render(request,'addnew.html',{'data':d})
    




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
            data=perfume.objects.all()
            if request.method=='POST':
                 v1 = request.POST.get('value1')  # returns None if not present
                 v2 = request.POST.get('value2')
                 
            
                 if v1 is not None and v2 is not None:
                    data = perfume.objects.filter(price__gt=v1, price__lte=v2)
                 
                
            if data.exists():
                context = {
                'head': 'for all customers',
                'data': data,
                    }
                return render(request, 'catalog.html', context)
            else:
                context = {'message': 'No items found in at this particular range'}
                return render(request, 'catalog.html', context)
            


def quantity(request):
    if request.method == 'POST':
        min_q = 0
        max_q = int(request.POST.get('value3', 0))
        print(max_q)

        data = perfume.objects.filter(quantity__gte=min_q, quantity__lte=max_q)
        
        

        return render(request, 'catalog.html', {
            'perfumes': data,
            
        })
    return render(request, 'catalog.html')

    
def serch(request):
    if request.method=='POST':
        value=request.POST.get['q']
        print(value)

    return render(request,'catalog.html')         

                     
                 
         
            

def men(request):
        list=[]
        d=PerfumeDetail.objects.filter(gender='M')  
        for i in d:
            item=i.perfume_id
            data=perfume.objects.filter(id=item)
            for i in data:
               list.append(i)
            print(list)
        context={
                 'head':'for men customers',
                 'data':list,
            }
        return render(request,'catalog.html',context)

def women(request):
        list=[]
        d=PerfumeDetail.objects.filter(gender='F')  
        for i in d:
            item=i.perfume_id
            data=perfume.objects.filter(id=item)
            for i in data:
               list.append(i)
        context={
                 'head':'for female customers',
                 'data':list,
            }
        return render(request,'catalog.html',context)
           
def unisex(request):
        list=[]
        d=PerfumeDetail.objects.filter(gender='U')  
        for i in d:
            item=i.perfume_id
            data=perfume.objects.filter(id=item)
            for i in data:
               list.append(i)
        context={
                 'head':'for unisex ',
                 'data':list,
            }
        return render(request,'catalog.html',context)
           
        
     

        

        

        

        # return render(request,'catalog.html',)

def viewall(request,id):
    data=perfume.objects.filter(id=id)

    
    d=PerfumeDetail.objects.filter(perfume_id=id)
    print(d)
    return render(request,'view.html',{'data':data,'d':d})



def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(login_view)
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(password)
            user = authenticate(request, username=username, password=password)  # check credentials
            if user is not None:
                login(request, user)  # log the user in
                messages.success(request, 'Logged in successfully!')
                return redirect(home)  # or any success URL
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect(login_view)
# def addtocart(request,id):
#     user=request.user

#     print(user)
#     print(id)
#     data=perfume.objects.filter(id=id)
#     if request.user.is_authenticated:
#         user_id = request.user.id
#     print(data)
#     name=data.name
#     price=data.price
#     img=data.img
#     d=Cart.objects.create(name=name,price=price,img=img,user_id=user_id)
#     d.save()
#     return render(request,'cart.html',{'user':user,'d':d})


def addtocart(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    try:
        perfume_obj = perfume.objects.get(id=id)
    except perfume.DoesNotExist:
        return HttpResponse("Perfume not found", status=404)
    
    name = perfume_obj.name
    price = perfume_obj.price
    img = perfume_obj.img
    product_id=id
    print(product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=user,
        name=name,
        defaults={'price': price, 'img': img,'product_id':product_id}
    )

    if created:
        cart_item.save()
        messages.success(request, "Item added to cart successfully!")
    else:
        messages.info(request, "Item is already in your cart.")

    # It’s better to redirect after POST, to avoid resubmission on refresh
    return redirect(home)



def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_id = request.user.id

    if request.method == "POST":
       
        delete_id = request.POST.get("delete_id")
        print(delete_id)
        if delete_id:
          Cart.objects.filter(id=delete_id).delete()
            # After deletion, redirect to avoid resubmission
          return redirect(cart_view)  # or the same URL name

    # For GET or other methods: show cart
    data = Cart.objects.filter(user_id=user_id)
    return render(request, 'cart.html', {'data': data})

def buynows(request,id):
    if request.user.is_authenticated:
      user_id = request.user.id
    product=perfume.objects.filter(id=id)
    details=PerfumeDetail.objects.filter(perfume_id=id)
    today=date.today()
    fdate = today + timedelta(days=5)
    for i in product:
        price=i.price
        pname=i.name
        img=i.img
    for i in details:
        stock=i.stock
        print(stock)
    if stock<=0:
        
        messages.info(request, "out of stock")
        return redirect(home)
    else:
        if request.method=='POST':
            name=request.POST['name']
            email=request.POST['email']
            gender=request.POST['gender']
            address=request.POST['address']
            state=request.POST['state']
            district=request.POST['district']
            pincode=request.POST['pincode']
            landmark=request.POST['landmark']
            order_date=request.POST['odate']
            delivered_date=request.POST['ddate']
            quantity=request.POST['quantity']
            if int(quantity) > stock:
                messages.info(request, "Out of stock")
                return redirect(home)
            else:
                 p=int(quantity)*price
                 data=Order.objects.create(user_id=user_id,address=address,full_name=name,email=email,gender=gender,state=state,district=district,pincode=pincode,landmark=landmark,order_date=order_date,delivered_date=delivered_date,totalprice=p,product_id=id,product_name=pname,quantity=quantity,img=img)
                 data.save()
                 PerfumeDetail.objects.filter(perfume_id=id).update(stock=F('stock') - int(quantity))
                 messages.info(request,"order succesfully")
                 message = (
                f"Hello {name}\n"
                "Thank you for visiting our site AURA perfumes\n"
                 "We have received your order and it's now confirmed. We will notify you once we start processing and shipping it.\n"
                f"Product Name: {pname}\n"
                f"Product Price: {p}\n"
                f"Quantity: {quantity}\n"
                f"Location: {address}\n"
                )
                 send_mail(
                subject='order confirmed',
                message=message,
                from_email='yadhuljaykumar@gmail.com',  # will use DEFAULT_FROM_EMAIL if None
                recipient_list=[email],
                fail_silently=False
                )
                 return redirect(home)
    return  render(request,'buynow.html',{'product':product,'details':details,'today':today,'fdate':fdate,'messages':messages,})
