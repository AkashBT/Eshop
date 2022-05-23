import email
from django.shortcuts import redirect, render,HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User

from .models.category import Category
# Create your views here.
from .models.product import Product
from .models.customer import Customer
from .models.orders import Order
from .models.payment import PaymentDetails
from .models.coupon import Coupon
from django.contrib.auth.hashers import make_password,check_password

from django.views import View
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from .models.review import Review
from .models.wishlist import Wishlist
from datetime import date
from django.template.loader import render_to_string

unique_id = get_random_string(length=32)

import razorpay

# from store.middlewares.auth import auth_middleware
class Index(View):
    def post(self,request):
        product=request.POST.get("product")
        remove=request.POST.get("remove")
        cart=request.session.get('cart')
        if cart:
            quantity =cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]=quantity-1

                else:
                    cart[product]=quantity+1
                
            else:
                cart[product]=1
        else:
            cart={}
            cart[product]=1

        request.session['cart']=cart
        print(request.session['cart'])
        return redirect("/")
    def get(self,request):
        if request.session.get('customer'):
            cart=request.session.get('cart')
            if not cart:
                request.session.cart={}
            products = None
            products = Product.get_all_products()
            category =Category.get_all_categories()
            user=Customer.objects.get(pk=request.session.get('customer')['id'])
            wishlist=Wishlist.objects.filter(customer=user)
            return render(request,'store/index.html',{'products':products,'category':category,'wishlistcount':wishlist})
        else:
            products=Product.objects.all()
            category=Category.objects.all()
            return render(request,'store/index.html',{'products':products,'category':category})


def dashboard(request):
        cart=request.session.get('cart')
        if not cart:
            request.session.cart={}
        products = None
        products = Product.get_all_products()
        category =Category.get_all_categories()
        user=Customer.objects.get(pk=request.session.get('customer')['id'])
        wishlist=Wishlist.objects.filter(customer=user)
        return render(request,'store/dashboard.html',{'products':products,'category':category,'wishlistcount':wishlist})
####### CUStomer Signup ###########################
def signup(request):
    if request.method=="GET":
        return render(request,'store/signup.html')
    else:
        customer=Customer()
        customer.username=request.POST.get('username')
        customer.fname=request.POST.get('fname')
        customer.lname=request.POST.get('lname')
        customer.email=request.POST.get('email')
        customer.phone=request.POST.get('phone')
        customer.address=request.POST.get('address')
        customer.password=make_password(request.POST.get('password'))
        customer.save()
        user=User()
        user.username=request.POST.get('username')
        user.password=make_password(request.POST.get('password'))
        user.save()
        return redirect('/')


class Login(View):
    return_url=None
    def get(self,request):
        if request.session.get('customer'):
            return redirect('store:dashboard')
        Login.return_url=request.GET.get('return_url')
        return render(request,'store/signin.html')
    
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            customer=Customer.objects.get(username=user.username)
            request.session['customer']={'id':customer.id,'fname':customer.fname,'lname':customer.lname,'email':customer.email,'phone':customer.phone,'address':customer.address}
            login(request, user)
            messages.info(request, f"You are now logged in as {email}.")
            # return render(request,"store/dashboard.html", {'customer': customer})
            return redirect('store:index')
        else:
            messages.error(request,"Invalid username or password.")
            return render(request,'store/signin.html')








########## logout ########################
def logout(request):
    request.session.clear()
    return redirect('store:signin')


######### Cart ##########################
class Carts(View):
    def get(self,request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        coupons=Coupon.objects.all()
        print(coupons,'-------------------------------')
        return render(request,'store/cart.html',{'products':products,'coupons':coupons})


# class Checkout(View):
    def post(self,request):
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        customer = request.session.get('customer')['id']
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))

        print(address,phone,customer,cart,products,'****************')
        
        for product in products:
            order = Order(
                    customer=Customer(id=customer),
                    product=product,
                    price=product.price,
                    quantity=cart.get(str(product.id)),
                    address = address,
                    phone=phone,
                    )
            order.placeOrder()
        
        request.session['cart']={}
        return redirect('store:cart')



######### orders ##########################
from django.utils.decorators import method_decorator
class OrderView(View):
    # @method_decorator(auth_middleware)
    def get(self,request):
        customer=request.session.get('customer')['id']
        orders=Order.get_order_by_customer(customer)
        return render(request,'store/order.html',{'orders':orders})


@csrf_exempt
def success(request):
    if request.session.get('customer'):
        if request.method == 'GET':
            
            return render(request,"store/success.html")
        else:
            address=request.session.get('customer')['address']
            phone=request.session.get('customer')['phone']
            customer = request.session.get('customer')['id']
            cart = request.session.get('cart')
            products = Product.get_products_by_id(list(cart.keys()))
            payment_status = "Success"
            payment_id=unique_id

            
            for product in products:
                order = Order(
                        customer=Customer(id=customer),
                        product=product,
                        price=product.price,
                        quantity=cart.get(str(product.id)),
                        address = address,
                        phone=phone,
                        )
                order.placeOrder()
                
            
            request.session['cart']={}
            return render(request,"store/success.html") 
    else:
        return redirect('store:signin')




def read_all(request,pk):
    product = Product.objects.get(id=pk)
    category =Category.get_all_categories()
    allreviews=Review.objects.filter(product=product.name)
    if request.method=="POST":
        reviews=Review()
        reviews.review =request.POST.get('review')
        reviews.product=request.POST.get('productname')
        reviews.user=request.POST.get('userid')
        reviews.created=date.today()
        reviews.save()
    else:
        pass
    return render(request,'store/read_all.html',{'product':product,'category':category,'reviews':allreviews})


def category(request,pk):
    category=Category.objects.get(id=pk)
    print(category,'---------------------------------------')
    products=Product.objects.filter(category=category)
    print(products,'***********************************')
    allcategory=Category.objects.all()
    user=Customer.objects.get(pk=request.session.get('customer')['id'])
    wishlist=Wishlist.objects.filter(customer=user)
    return render(request,'store/index.html',{'products':products,'category':allcategory,'wishlistcount':wishlist})
    # return render(request,'store/category.html',{'products':products,'category':allcategory})

def add_wishlist(request,pk):
    if request.session.get('customer'):
        product=Product.objects.get(pk=pk)
        user=Customer.objects.get(pk=request.session.get('customer')['id'])
        wishlist=Wishlist()
        wishlist.product=product
        wishlist.customer=user
        wishlist.save()
        return redirect('store:index')
    else:
        return redirect('store:signin')

def wishlist(request):
    if request.session.get('customer'):
        user=Customer.objects.get(pk=request.session.get('customer')['id'])
        wishlists=Wishlist.objects.filter(customer=user)
        return render(request,'store/wishlist.html',{'wishlists':wishlists})
    else:
        return redirect('store:signin')



def removewishlist(request,pk):
    if request.session.get('customer'):
        list=Wishlist.objects.get(pk=pk)
        list.delete()
        return redirect('store:wishlist')
    else:
        return redirect('store:signin')



def search(request):
    category =Category.get_all_categories()
    search=request.GET.get('search')
    products = Product.objects.filter(category__name__icontains=search)
    
    print(search)
    return render(request,'store/search.html',{'category':category,'search':search,'products':products})


def invoice(request,pk):
    if request.session.get('customer'):
        customer=Customer.objects.get(id=request.session.get('customer')['id'])
        orders=Order.objects.get(id=pk)
        print(orders,'--------------------------------')
        # return render(request,'store/invoice.html',{'order':orders,'customer':customer})
        rendered = render_to_string('store/invoice.html', {'order':orders,'customer':customer})
        return HttpResponse(rendered)
    else:
        return redirect('store:signin')

def popup(request):
    return render(request,'store/popup.html')