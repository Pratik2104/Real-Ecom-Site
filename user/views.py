from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import userRegistrationForm
from django.contrib.auth.decorators import login_required
from shop.models import Product
from .models import Cart,Wishlist,Order
from django.urls import reverse

# Create your views here.
def register(request):
    if request.method=='POST':
        my_form = userRegistrationForm(request.POST)
        if my_form.is_valid():
            my_form.save()
            username = my_form.cleaned_data.get('username')
            messages.success(request,f'Welcome {username}, your account has been registered!!')
            return redirect('login')
    else:
        my_form = userRegistrationForm()
    return render(request,'user/register.html',{'form':my_form})


@login_required
def UserProfilePage(request):
    return render(request,"user/profile.html")

@login_required
def addtowishlist(request,id):
    user = request.user
    product = Product.objects.get(id=id)
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    wishlist.products.add(product)
    return redirect('home')

@login_required
def addtocart(request,id):
    user = request.user
    product = Product.objects.get(id=id)
    cart, created = Cart.objects.get_or_create(user=user)
    cart.products.add(product)
    return redirect('cart')


def movetocart(request,id):
    user = request.user
    product = Product.objects.get(id=id)
    cart, created = Cart.objects.get_or_create(user=user)
    cart.products.add(product)

    # This can be done in a simple way by using absolute url as well. Used this way to show how to use named url pattern while also passing a parameter. 
    string_id = str(id)
    remove_form_wishlist_url = reverse('removefromwishlist',kwargs={'id':string_id})
    return redirect(remove_form_wishlist_url)


def wishlist(request):
    if request.user.is_authenticated :
        user = request.user
        wishlist = Wishlist.objects.get(user=user)
        products = wishlist.products.all()
        return render(request,'user/wishlist.html',{'product_list':products})
    return render(request,'user/wishlist.html')


def cart(request):
    if request.user.is_authenticated :
        user = request.user
        cart = Cart.objects.get(user=user)
        products = cart.products.all()
        total=0
        for product in products:
            total+=product.discount_price
        return render(request,'user/cart.html',{'product_list':products,'subtotal':total})
    return render(request,'user/cart.html')


def removefromwishlist(request,id):
    user = request.user
    product = Product.objects.get(id=id)
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    wishlist.products.remove(product)
    return redirect('wishlist')


def removefromcart(request,id):
    user = request.user
    product = Product.objects.get(id=id)
    cart, created = Cart.objects.get_or_create(user=user)
    cart.products.remove(product)
    return redirect('cart')

@login_required
def checkout(request):
    if request.method == "POST" :
        name = request.POST.get("name","")
        email = request.POST.get("email","")
        city = request.POST.get("city","")
        state = request.POST.get("state","")
        address = request.POST.get("address","")
        address2 = request.POST.get("address2","")
        zipcode = request.POST.get("zipcode","")
        user = request.user
        cart = Cart.objects.get(user=user)
        product_list = cart.products.all()
        total=0
        for product in product_list:
            total+=product.discount_price
            cart.products.remove(product)
        order = Order(user=user,name=name,address=address,address2=address2,city=city,state=state,zipcode=zipcode,email=email)
        order.save()
        order.products.set(product_list)
        return render(request,'user/order_success.html')
    else :
        user = request.user
        cart = Cart.objects.get(user=user)
        products = cart.products.all()
        total=0
        for product in products:
            total+=product.discount_price
        return render(request,'user/checkout.html',{'products':products,'total':total})