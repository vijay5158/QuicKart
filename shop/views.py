from django.shortcuts import render,redirect,HttpResponse
from .models import OrderProd, Product , Contact, Orders, CustomUser, Address
from math import ceil
from django.contrib import messages 
from django.contrib.auth.models import User 
from django.contrib.auth  import authenticate,  login, logout
import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def Home(request):
    
    allProds = []
    catprods = Product.objects.values('prod_category', 'prod_id')
    cats = {item['prod_category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(prod_category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds':allProds}
    return render(request, 'home.html', params)


def About(request):
    return render(request, 'about.html')

def Contact(request):
    if request.method == "POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        contactus = Contact(name=name,email=email,phone=phone,desc=desc)
        contactus.save()

    return render(request, 'contact.html')

def Tracker(request):
    order_id = request.GET.get('order_id')
    if order_id is not None:
        orders = [Orders.objects.filter(order_id=order_id).filter(user=request.user).first()]
        status = orders[0].status
        if orders[0]==None:
            messages.error(request,'Order Does not exist')
            return redirect('TrackingStatus')
        all_prods = []
        for product in orders[0].products.all():
            all_prods.append([product.product.prod_img,product.product.prod_name,product.quantity,product.get_total_prod_price()])
        return render(request, 'tracker.html',{'status':status,'orders':orders,'order_detail':True,'products':all_prods})
    orders = [Orders.objects.filter(user=request.user)]
    return render(request, 'tracker.html',{'orders':orders,'order_detail':False})

def search_match(searches, product):
    searches_list = searches.split(" ")
    match = 0
    for search in searches_list:
        if search.lower() in product.prod_name.lower() or search.lower() in product.prod_category.category.lower() or search.lower() in product.prod_desc.lower():
            match+=1
    if match>=1:
        return True
    else:
        return False

def Search(request):
    searches = request.GET.get('search','')
    allProds = []
    catprods = Product.objects.values('prod_category', 'prod_id')
    cats = {item['prod_category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(prod_category=cat)
        prod = [product for product in prodtemp if search_match(searches, product)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(searches)<4:
        params = {'msg': "Please make sure to enter relevant search query"}    
    return render(request, 'home.html', params)

def ProductView(request, id):
    product = Product.objects.filter(prod_id=id)
    
    return render(request, 'productview.html',{'product' : product[0]})

def Checkout(request,items_list=[]):
    if len(items_list) >0:
        item_ids = [int(item) for item in items_list.split(',')]
        cart_items = [Product.objects.filter(prod_id=item_id) for item_id in item_ids]
        return render(request, 'checkout.html',{'cart_items': cart_items})
    else:
        return render(request, 'checkout.html')

def ConfirmOrder(request):
    if request.method=="GET":
        addresses = request.user.address.all()
        
        if addresses is None:
            address_status=False
            return render(request,'address.html',{'address_status':address_status})
        else:
            address_list = [Address.objects.filter(id=address.id) for address in addresses]
            return render(request,'address.html',{'address_status':address_list})
    if request.method=="POST":
        existing_address = request.POST.get('existing_add','')
        
        items_json= request.POST.get('items_json', '')
        total_price= request.POST.get('total_price', '')
        if existing_address == 'False':
            
            name=request.POST.get('name', '')
            email=request.POST.get('email', '')
            address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
            city=request.POST.get('city', '')
            state=request.POST.get('state', '')
            zip_code=request.POST.get('zip_code', '')
            phone=request.POST.get('phone', '')
            user_address= Address.objects.create(name=name,email=email,
            address=address,city=city,state=state,zip_code=zip_code,phone=phone)
            request.user.address.add(user_address.id)
        else:
            user_address= Address.objects.filter(id=existing_address).first()
        payment_mode=request.POST.get('payment', '')
        
        order = Orders(user=request.user,total_price=float(total_price), address= user_address,payment_mode=payment_mode)
        order.save()
        prod_dict = json.loads(items_json)
        for prod_id in prod_dict:
            product = Product.objects.filter(prod_id=prod_id).first()
            if product is not None:
                
                order_prod = OrderProd.objects.create(product=product,quantity=int(prod_dict[prod_id][0]))
                if order_prod is None:
                    return HttpResponse('error')
                order.products.add(order_prod.id)

                # except:
                #     return HttpResponse('error')


        order.save()
        thank=True
        address_status=False
        id=order.order_id
        return redirect('OrderSuccess',id=int(id))
    return render(request,'address.html',{'address_status':False})


def Login(request):
    if request.method=="POST":
        loginemail=request.POST['loginemail']
        loginpassword=request.POST['loginpassword']

        user=authenticate(email= loginemail, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("Home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("Home")

    return HttpResponse("404- Not found")


def Signup(request):
    if request.method=="POST":
        signupemail=request.POST['signupemail']
        fname=request.POST['first-name']
        lname=request.POST['last-name']
        pass1=request.POST['password1']
        pass2=request.POST['password2']

        if (pass1!= pass2):
            messages.error(request, " Passwords do not match")
            return redirect('Home')

        myuser = CustomUser.objects.create_user(signupemail, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your account has been successfully created")
        return redirect('Home')

    else:
        return HttpResponse("404 - Not found")
    


def Logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('Home')    

@login_required
def OrderSuccess(request,id=None):
    thank=True
    order = Orders.objects.filter(order_id=id).filter(user=request.user).first()
    total_price = order.total_price
    payment_mode = order.payment_mode
    date = order.date
    return render(request, 'ordersuccess.html', {'thank':thank, 'id':id,'total_price':total_price,'date':date,'payment_mode':payment_mode})
