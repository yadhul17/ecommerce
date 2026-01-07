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
from django.http import JsonResponse


User = get_user_model()

# admin

# def admin_dashboard(request):
#     return render(request, "dashboard.html")

# def admin_perfume_list(request):
#     perfumes = perfume.objects.all()
#     return render(request, "admin/perfume_list.html", {"perfumes": perfumes})

# # Add perfume
# def admin_perfume_add(request):
#     form = PerfumeForm(request.POST or None, request.FILES or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return redirect("admin_perfume_list")
#     return render(request, "admin/perfume_form.html", {"form": form})

# # Edit perfume
# def admin_perfume_edit(request, pk):
#     item = get_object_or_404(perfume, pk=pk)
#     form = PerfumeForm(request.POST or None, request.FILES or None, instance=item)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return redirect("admin_perfume_list")
#     return render(request, "admin/perfume_form.html", {"form": form})

# # Delete perfume
# def admin_perfume_delete(request, pk):
#     item = get_object_or_404(perfume, pk=pk)
#     if request.method == "POST":
#         item.delete()
#         return redirect("admin_perfume_list")
#     return render(request, "admin/confirm_delete.html", {"item": item})






def index(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        

        if(username=='admin'and password=='admin@123'):
            return redirect("adminlist")


        # If credentials are correct and user is staff, log them in
       
    return render(request,"dashboard.html")

def adminlist(request):
    return render (request,'adminview.html')
   
def allproduct(request):
    products = perfume.objects.all()
    return render(request, "allproduct.html", {"products": products})
def admin_perfume_add(request):
    if request.method=='POST':
        file1 = request.FILES.get('image')
        name = request.POST['name']
        price = request.POST['price']
        about = request.POST['about']
        gender = request.POST['gender']
        stock = request.POST['stock']

        data = perfume.objects.create(img=file1, name=name, price=price)
        PerfumeDetail.objects.create(perfume=data, about=about, gender=gender, stock=stock)

        return redirect('adminlist')
    return render(request,"adds.html")
def admin_perfume_edit(request):
    return render(request,"dashboard.html")
def admin_perfume_delete(request, pk):
    # fetch the object (or return 404 if not found)
    obj = get_object_or_404(perfume, pk=pk)
    
    # only delete on POST
    if request.method == "POST":
        obj.delete()
        return redirect("adminlist")  # redirect to products page

    # (Optional) If you want a confirmation page:
    return render(request, "allproduct.html", {"object": obj})



def alluser(request):
    users=User.objects.all()
    
    return render(request,'users.html',{"users":users})

def allorder(request):
    orders=Order.objects.all()
    
    
    return render(request,'orderss.html',{"orders":orders})
# Create your views here.
def home(request):
    data = perfume.objects.all().order_by('-id')[:4]  # e.g. last 4 entries
    data = data.prefetch_related('details')

    d=new.objects.all()[:4]
    user = request.user
    print(user)
    if not user.is_authenticated:
        return redirect(login_view)  
    



   

    return render(request ,'home.html',{'data':data,'d':d})


# def adminlogin(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         try:
#             user = User.objects.get(email=email)
#             print(user.email)
#         except User.DoesNotExist:
#             user = None

#         if user is not None and user.check_password(password):
#             login(request,user)
#             return redirect(adddetails)
           

#     return render(request, 'admin.html')
# def adminlogin(request):
#     user = request.user
#     if user is not None:
#         return render(request,'')

def adddetail(request):
    if not request.user.is_authenticated:   
        return redirect(login_view)
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
        return redirect(login_view)
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
    perfumes = perfume.objects.all()  # always return queryset

    if request.method == 'POST':
        try:
            max_stock = int(request.POST.get('value3', 0))
        except ValueError:
            max_stock = 0

        perfumes = perfumes.filter(details__stock__lte=max_stock)
        print(perfumes)
        if perfumes.exists():
                context = {
                'head': 'for all customers',
                'data': perfumes,
                    }
                return render(request, 'catalog.html', context)
        else:
                context = {'message': 'No items found in at this particular range'}
                return render(request, 'catalog.html', context)


   


    
# def serch(request):
#     if request.method=='POST':
#         value=request.POST.get['q']
#         print(value)

#     return render(request,'catalog.html')         

                     
                 
         
            

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
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:   # or user.is_superuser, or your own role flag
                return redirect(adddetails)
            else:
                return redirect(home)
        else:
            messages.error(request, 'Invalid credentials')
    return render(request,'login.html')
    


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


from django.shortcuts import redirect, HttpResponse
from django.contrib import messages

def addtocart(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user

    # try to get the perfume
    try:
        perfume_obj = perfume.objects.get(id=id)
    except perfume.DoesNotExist:
        return HttpResponse("Perfume not found", status=404)

    # now get the related perfume details
    try:
        details = PerfumeDetail.objects.get(perfume=perfume_obj)
    except PerfumeDetail.DoesNotExist:
        return HttpResponse("Product details not found", status=404)

    # check stock
    if details.stock <= 0:
        messages.error(request, "Sorry! This product is out of stock.")
        return redirect('home',)

    # proceed with adding to cart
    name = perfume_obj.name
    price = perfume_obj.price
    img = perfume_obj.img
    product_id = id

    cart_item, created = Cart.objects.get_or_create(
        user=user,
        name=name,
        defaults={'price': price, 'img': img, 'product_id': product_id}
    )

    if created:
        # optionally reduce stock in perfumedetails
        
        cart_item.save()

        messages.success(request, "Item added to cart successfully!")
    else:
        messages.info(request, "Item is already in your cart.")

    return redirect('home')



def addtoWish(request,id):
    return redirect('home')

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


# serch
from django.db.models import Q

def serch(request):
    query = request.GET.get('q', '').strip()
    print(query)

    if query:
        data = perfume.objects.filter(name__icontains=query)
        if not data.exists():
            print("no related data")
        else:
            print("Found:", data)
    else:
        data = perfume.objects.all()

    return render(request, 'catalog.html', {'results': data, 'query': query})