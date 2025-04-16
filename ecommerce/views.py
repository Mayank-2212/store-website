from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import *
from . models import *
from accounts.models import *
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="signin")
def home(request):
    fetch_products = Products.objects.all()
    for product in fetch_products:
        product_images = ProductImage.objects.filter(product=product)
    print(product_images)
    context = {'products':fetch_products}
    return render(request, 'home.html',context)
 

def remove(request,id):
        product = CartItems.objects.get(id=id).delete()
        return redirect('cart_details')
    
def details(request , product_slug):
    product = Products.objects.get(slug=product_slug)

    
    product_images = ProductImage.objects.filter(product=product)
    context = {'product':product,'product_images':product_images}

    if request.GET.get('size'):
        size = request.GET.get('size')
        price =product.get_product_price_by_size(size)
        context['updated_price'] = price
        context['selected_size'] = size

    return render(request,'details.html' , context )


@login_required(login_url="signin")
def cart(request , product_slug):

    try:
        product = Products.objects.get(slug=product_slug)
    except Products.DoesNotExist:
        # Handle case where product_slug is not found
        return HttpResponseNotFound("Product not found")

    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

    try:
        fetch_item = CartItems.objects.filter(cart=cart , product=product).first()

        if fetch_item:
            fetch_item.quantity += 1
            fetch_item.total_price += product.price
            fetch_item.save()
        else: 
            cart_items = CartItems.objects.create(cart=cart, product=product,total_price = product.price)
    except Exception as e:
        # Handle any other exceptions that may occur
        return HttpResponseServerError("Error creating cart item: {}".format(e))

    if request.GET.get('variant'):
        try:
            variant = request.GET.get('variant')
            size_variant = SizeVariant.objects.get(size_name=variant)
            cart_items.size_variant = size_variant
            cart_items.save()
        except SizeVariant.DoesNotExist:
            # Handle case where variant is not found
            return HttpResponseNotFound("Variant not found")

    return redirect("details",product_slug=product_slug)

@login_required(login_url="signin")
def cart_details(request):
    print("here")
    cart_item = CartItems.objects.filter(cart__user=request.user,cart__is_paid=False)
    cart = Cart.objects.get(user=request.user,is_paid=False)

    total = 0
    
    for item in cart_item:
       
        total += item.sub_total()

    
    
    context = {
        'cart_items':cart_item,
        'cart':cart,
        "total" : total,
        "final_total": total+10
    }
    return render(request,'cart_details.html',context)

@login_required(login_url="signin")
def store(request):
    
    products = Products.objects.all()
    count = len(products)
    context = {
        'products':products,
        'count':count
        }
    return render(request,"store.html",context)

@login_required(login_url="signin")
def plus(request,id):
    cart = CartItems.objects.get(id=id)
    cart.quantity += 1
    cart.save()
    return redirect("cart_details")

@login_required(login_url="signin")
def minus(request,id):
    cart = CartItems.objects.get(id=id)
    cart.quantity -= 1
    cart.save()
    return redirect("cart_details")

@login_required(login_url="signin")
def checkout(request):

    cart_item = CartItems.objects.filter(cart__user=request.user,cart__is_paid=False)
    cart = Cart.objects.get(user=request.user,is_paid=False)
    print(cart_item)

    total = 0
    
    for item in cart_item:
       
        total += item.sub_total()

    
    
    context = {
        'cart_items':cart_item,
        'cart':cart,
        "total" : total,
        "final_total": total+10
    }
    return render(request,'checkout.html',context)

@login_required(login_url="signin")
def place_order(request):
    cart = Cart.objects.get(user=request.user,is_paid=False)
    cart.is_paid = True
    cart.save()
    return render(request,'place_order.html',{'cart':cart})