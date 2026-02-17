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
from django.conf import settings
import razorpay
import json
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from datetime import date





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
    username = None
    password = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # only check login on POST
        if username == 'admin' and password == 'admin@123':
            return redirect("adminlist")

    return render(request, "dashboard.html")

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
def admin_perfume_edit(request, id):
    # 1. Fetch the main perfume object
    product = get_object_or_404(perfume, pk=id) 
    
    # 2. Fetch the related details (assuming the FK/OneToOne field is named 'perfume')
    # If your detail model doesn't exist for this product yet, we handle that too
    details = get_object_or_404(PerfumeDetail, perfume=product)

    if request.method == "POST":
        # Extract data from the HTML form
        name = request.POST.get('name')
        price = request.POST.get('price')
        gender = request.POST.get('gender')
        stock = request.POST.get('stock')
        description = request.POST.get('description') 
        image = request.FILES.get('img')

        if name:
            # Update Main Model
            product.name = name
            product.price = price
            if image:
                product.img = image
            product.save()

            # Update Details Model
            details.stock = stock
            details.gender = gender
            details.about = description # Or details.description depending on your field name
            details.save()

            messages.success(request, f"Product '{name}' and its details updated!")
            return redirect('adminlist')
        else:
            messages.error(request, "The Name field is required.")

    # Pass BOTH objects to the template
    return render(request, 'edit.html', {
        'perfumes': product,
        'details': details
    })
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
    # Just fetch all orders. 'status' is already a column in this table now.
    orders = Order.objects.all().order_by('-id')
    
    # We don't need the 'for order in orders' loop anymore 
    # because 'order.status' exists by default.
    
    return render(request, 'orderss.html', {"orders": orders})
def update_order_status(request,id):
    if request.method == 'POST':
     
        new_status = request.POST.get('new_status')
        
        order = get_object_or_404(Order, id=id)
        order.status = new_status
        
        # Intern Logic: If the status is 'Delivered', you might want to 
        # set the delivered_date automatically!
        if new_status == "Delivered":
            from datetime import date
            order.delivered_date = date.today().strftime("%Y-%m-%d")
            
        order.save()
        messages.success(request, f"Order #{id} updated to {new_status}")
        
    return redirect('orders')


# def update_order_status(request, order_id):
#     if request.method == 'POST':
#         order = get_object_or_404(Order, id=order_id)
#         # Get status from form, default to current if somehow missing
#         new_status = request.POST.get('status')

#         # Logic: If manually set to Delivered, OR if the date is today
#         # We use .capitalize() or similar to keep data consistent
#         if new_status == 'Delivered' or order.delivered_date == date.today():
#             new_status = 'Delivered'
#             order.delivered_date = date.today()
#             order.save(update_fields=['delivered_date'])

#         # Create the history record
#         # Note: Ensure your UPDATE model field is 'orders' (plural) as per your code
#         UPDATE.objects.create(
#             user=request.user,
#             orders=order,
#             status=new_status
#         )

#     return redirect("orders")





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
       
             
        
        return render(request,'addnew.html',{'d':d})
    




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
        username = request.POST.get("username").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()

        # All fields required
        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return redirect("register")

        # Username exists?
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("register")

        # Email exists?
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        # Create user and hash password
        user = User.objects.create_user(username=username, email=email, password=password)

        # Log user in
        login(request, user)

        # Success message
        messages.success(request, "Account created successfully!")

        # Redirect to home page
        return redirect("home")

    return render(request, "register.html")
   


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # redirect based on staff status
            if user.is_staff:  
                return redirect("adddetails")  # use quotes for URL name
            else:
                return redirect("home")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "login.html")


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
def cancel_order(request, id):
    # REMOVE the 'if request.method == "POST"' line
    order = get_object_or_404(Order, id=id, user=request.user)

    # 1. Validation
    if order.status == "Cancelled":
        messages.error(request, "Order already cancelled.")
        return redirect('profile')

    # Note: Use your status field check if 'is_shipped' isn't a real boolean field
    if order.status in ["Shipped", "Delivered"]:
        messages.error(request, "Cannot cancel order that has been shipped or delivered.")
        return redirect('profile')

    # 2. Update Status
    order.status = "Cancelled"
    order.save()

    # 3. Refund Logic
    try:
        payment_id = Payment.payment_id
        if payment_id: # Only try refund if a payment ID exists
            # Ensure your amount matches the field name (order.totalprice?)
            refund = settings.razorpay_client.refund.create({
                "payment_id": payment_id,
                "amount": int(order.totalprice * 100) # Razorpay/Stripe use paise/cents
            })
            order.refund_id = refund["id"]
            order.refund_status = "initiated"
            order.save()
            messages.success(request, "Order cancelled and refund initiated.")
        else:
            messages.success(request, "Order cancelled (No payment found to refund).")
            
    except Exception as e:
        print(f"Refund Error: {e}") # Look at your terminal to see why it fails
        messages.error(request, f"Order cancelled — refund failed: {str(e)}")
        
    return redirect('profile')


def profile(request):
    # 1. Fixed: Removed .prefetch_related('update_set') since the model doesn't exist yet
    # Also fixed: Filter by 'user' (singular) to match your Order model
    orders = (
        Order.objects
        .filter(user=request.user)
        .order_by('-id')
    )
    order_count = orders.exclude(status="Cancelled").count()
    # 2. Simplified Status Logic
    # Since you don't have an 'Update' model yet, let's just default to "Pending"
    for order in orders:
        order.current_status = "Pending" 

    
    # 3. Fixed: Filter by 'users' (plural) to match your Wish model
    wish_count = Wish.objects.filter(users=request.user).count()

    # Debugging
    print(f"User {request.user.username} has {wish_count} items in wishlist")

    # 4. Profile handling (Using singular 'user' as per your Profile model)
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.full_name = request.POST.get('full_name', '').strip()
        profile.phone = request.POST.get('phone', '').strip()
        profile.dob = request.POST.get('dob')
        profile.save()

        email = request.POST.get('email', '').strip()
        if email:
            request.user.email = email
            request.user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'profile.html', {
        'profile': profile,
        'order_count': order_count,
        'orders': orders,
        'wish_count': wish_count # Added this so it shows in your template
    })

def delete(request,id):
    order=Order.objects.filter(id=id).delete()
    
    return redirect('profile')

def addtocart(request,id):
    
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
        Cart.objects.filter(user=user, product_id=id).delete()
        messages.error(request, "This product is out of stock and has been removed from your cart.")
        return redirect('home')

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



def addtoWish(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user

    try:
        perfume_obj = perfume.objects.get(id=id)
    except perfume.DoesNotExist:
        return HttpResponse("Perfume not found", status=404)

    try:
        details = PerfumeDetail.objects.get(perfume=perfume_obj)
    except PerfumeDetail.DoesNotExist:
        return HttpResponse("Product details not found", status=404)

    Wish_item, created = Wish.objects.get_or_create(
        users=user,           
        perfume=perfume_obj
    )

    if created:
        Wish_item.save()
        messages.success(request, "Item added to wish successfully!")
    else:
        messages.info(request, "Item is already in your wishlist.")

    return redirect('home')

def wish_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_id = request.user.id

    if request.method == "POST":
       
        delete_id = request.POST.get("delete_id")
        print(delete_id)
        if delete_id:
          Wish.objects.filter(id=delete_id).delete()
            # After deletion, redirect to avoid resubmission
          return redirect('home')  # or the same URL name

    # For GET or other methods: show cart
    data = Wish.objects.filter(users_id=user_id)
    print(data)
    return render(request, 'wishlist.html', {'data': data})

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

from django.db.models import F


def buynows(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to buy.")
        return redirect('login')

    user = request.user

    product = perfume.objects.filter(id=id)
    details = PerfumeDetail.objects.filter(perfume_id=id)

    today = date.today()
    fdate = today + timedelta(days=5)

    # unpack product info
    for i in product:
        price = i.price
        pname = i.name
        img = i.img

    # unpack stock
    stock = 0
    for i in details:
        stock = i.stock

    if stock <= 0:
        messages.info(request, "Out of stock")
        
        return redirect('home')

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        gender = request.POST['gender']
        address = request.POST['address']
        state = request.POST['state']
        district = request.POST['district']
        pincode = request.POST['pincode']
        landmark = request.POST['landmark']
        order_date = request.POST['odate']
        delivered_date = request.POST['ddate']
        payment_mode = request.POST.get("payment_mode")
        quantity = request.POST['quantity']

        # check stock quantity
        if int(quantity) > stock:
            messages.info(request, "Quantity exceeds stock")
            return redirect('home')

        total_price = int(quantity) * price
        order = Order.objects.create(
            user_id=user.id,
            address=address,
            full_name=name,
            email=email,
            gender=gender,
            state=state,
            district=district,
            pincode=pincode,
            landmark=landmark,
            payment_mode=payment_mode,
            order_date=order_date,
            delivered_date=delivered_date,
            totalprice=total_price,
            product_id=id,
            product_name=pname,
            quantity=quantity,
            img=img
        )

        order.save()
        message = (
            f"Hello {name},\n"
            "Thank you for ordering from AURA perfumes.\n"
            f"Product Name: {pname}\n"
            f"Total Price: {total_price}\n"
            f"Quantity: {quantity}\n"
            f"Address: {address}\n"
        )
        send_mail(
            subject='Order Confirmed',
            message=message,
            from_email='yadhuljaykumar@gmail.com',
            recipient_list=[email],
            fail_silently=False
        )

        

        # if payment mode is online/card, redirect to payment
        if payment_mode in ['card_upi', 'Card / UPI']:
            # pass necessary data to payment page (like via session or query params)
            request.session['order_id'] = order.id
            PerfumeDetail.objects.filter(perfume_id=id).update(stock=F('stock') - int(quantity))
              
            
            return redirect('payment')  # payment view name

        # else if cash on delivery or others — save order immediately
    

        # decrease stock
        PerfumeDetail.objects.filter(perfume_id=id).update(stock=F('stock') - int(quantity))

        messages.success(request, "Order placed successfully .")

        
        
        return redirect('home')
    
    return render(request, 'buynow.html', {
        'product': product,
        'details': details,
        'today': today,
        'fdate': fdate,
    })


def payments(request):
    print("Razorpay Key ID:", settings.RAZORPAY_KEY_ID)
    print("Razorpay Key Secret:", settings.RAZORPAY_KEY_SECRET)
    
   # get order_id from session
    order_id = request.session.get('order_id')
    if not order_id:
        messages.error(request, "No order found to pay for.")
        return redirect("home")

    # fetch the Order object (your own model)
    order_obj = get_object_or_404(Order, id=order_id)

    order_amount = order_obj.totalprice
    order_name = order_obj.full_name

    if request.method == "POST":
        # initialize razorpay client
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        # create a Razorpay order using the amount
        razorpay_order = client.order.create({
            "amount": int(order_amount) * 100,  # in paise
            "currency": "INR",
            "receipt": f"order_{order_obj.id}"
        })
        razorpay_order_id = razorpay_order["id"]

        # create a payment record in your database
        payment_record = Payment.objects.create(
            users=request.user,
            orders=order_obj,
            amount=order_amount,
            provider_order_id=razorpay_order_id,
            payment_id="",      # will update after callback
            signature_id="",    # will update after callback
        )

        # pass to template
        context = {
            "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/",

            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "razorpay_order_id": razorpay_order_id,
            "order_obj": order_obj,
            "order_name": order_name,
            "order_amount": order_amount,
            "payment_record": payment_record,
        }
        return render(request, "payment.html", context)

    

    # GET request: show payment page
    return render(request, "payment.html", {
        "order_obj": order_obj,
        "order_name": order_name,
        "order_amount": order_amount
    })


@csrf_exempt
def callback(request):
    
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    if request.method == "POST" and "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id")
        provider_order_id = request.POST.get("razorpay_order_id")
        signature_id = request.POST.get("razorpay_signature")

        # Get the Payment record using razorpay_order_id
        payment_record = get_object_or_404(Payment, provider_order_id=provider_order_id)

        # Assign values from the POST
        payment_record.payment_id = payment_id
        payment_record.signature_id = signature_id

        params_dict = {
            "razorpay_order_id": provider_order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature_id,
        }

        try:
            # Verify payment signature
            client.utility.verify_payment_signature(params_dict)

            # If signature verification passes, mark as success
            payment_record.status = "SUCCESS"
            payment_record.save()

            return render(request, "callback.html", {"status": "Success"})

        except razorpay.errors.SignatureVerificationError:
            # If verification fails
            payment_record.status = "FAILED"
            payment_record.save()
            return render(request, "callback.html", {"status": "Failed"})

    # If missing signature or not POST
    return render(request, "callback.html", {"status": "Invalid request"})



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