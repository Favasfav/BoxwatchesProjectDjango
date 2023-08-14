from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from accounts.models import *
from django.contrib import messages
import random
from django.conf import settings
from django.contrib.auth.models import User
from products.models import * 
from carts.models import * 
from datetime import date
from django.urls import reverse
from .models import Cart, CartItem,Coupons

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST









@login_required(login_url='login_user')
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    colors = ProductVariation.objects.filter(product=product, variation_category='color')
    types = ProductVariation.objects.filter(product=product, variation_category='item_type')

    context = {
        'product': product,
        'colors': colors,
        'types': types,
    }
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    
    if product.stock <= 0:
        messages.warning(request, 'This product is out of stock.')
        return redirect('cart')

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, 'Product added Successfully.')
        
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1,
        )
        cart_item.save()
        messages.success(request, 'Product added to the cart.')

    return redirect('cart')



@login_required(login_url='login_user')
@require_POST
def update_quantity(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        item_id = request.POST.get('item_id')
        new_quantity = int(request.POST.get('new_quantity', 1))

        try:
            cart_item = get_object_or_404(CartItem, id=item_id)
            if new_quantity <= 0:
                cart_item.delete()
            else:
                cart_item.quantity = new_quantity
                cart_item.save()
                messages.success(request, 'Product added to the cart.')

            # Recalculate the sub-total and cart total
            item_sub_total = cart_item.product.price * cart_item.quantity

            cart = cart_item.cart
            cart_items = cart.cartitem_set.filter(is_active=True)  # Update this query if needed
            cart_total = sum(item.product.price * item.quantity for item in cart_items)

            return JsonResponse({
                'success': True,
                'item_sub_total': item_sub_total,
                'cart_total': cart_total
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})







    

@login_required(login_url='login_user')
def cart(request):
    total = 0
    cart = None
    cart_items = None
       
    try:
        user = request.user
        cart = Cart.objects.get(user=user, is_paid=False)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        print('hfyfy',cart.id)
        
        
        
        for item in cart_items:
            total += (item.product.price * item.quantity)
    except Cart.DoesNotExist:
        pass
    
             
            
            
        
    context = {
        'total': total,
        'cart': cart,
        'cart_items': cart_items,
        # 'coupons':coupons
    }
    
    return render(request, 'user/cart.html', context)

@login_required(login_url='login_user')
def reduce_quantity(request,product_id):
    user=request.user
    cart=Cart.objects.get(user_id= user)
    product = Product.objects.get(id=product_id)
    cart_items = CartItem.objects.get(cart=cart,product=product)
    
   
    if cart_items.quantity>1:
        cart_items.quantity-=1
        cart_items.save()
        messages.success(request, 'Product quantity is changed.')
    else:
        cart_items.delete()    
    return redirect('cart')    
        
    
@login_required(login_url='login_user')
def remove_cart(request, cartitem_id):
  
        cart_item = CartItem.objects.get(id=cartitem_id)
        cart_item.delete()
        messages.success(request, 'CartItem removed from Cart')
        return redirect('cart')
 
# views.py




@login_required(login_url='login_user')
def checkout(request, cart_id):
    total = 0
    cart = None
    tax = 0
    adresses = None
    coupon_obj = None
    

    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user, is_paid=False)
        except Cart.DoesNotExist:
            pass
        else:
            coupon_code = request.POST.get('coupon_code')
            coupon_obj = Coupons.objects.filter(coupon_code__iexact=coupon_code).first()

            if not coupon_obj:
                messages.warning(request, 'Invalid coupon.')
                return redirect('checkout',cart_id=cart.id)

            # if cart.coupon:
            #     messages.warning(request, 'Coupon already exists OR used before.')
            #     return redirect('checkout',cart_id=cart.id)

            if coupon_obj.is_expired:
                messages.warning(request, 'Coupon has been expired.')
                return redirect('checkout',cart_id=cart.id)

            cart.coupon = coupon_obj
            
            cart.save()
            messages.success(request, 'Coupon Applied Successfully.')

    try:
        user = request.user
        cart = Cart.objects.get(user=user, is_paid=False)
        adresses = Adress.objects.filter(user=user)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for item in cart_items:
            total += (item.product.price * item.quantity)

        if coupon_obj:
            if total < coupon_obj.minimum_amount:
                messages.warning(request, f"Amount should be greater than {coupon_obj.minimum_amount}")
                return redirect('checkout',cart_id=cart.id)
            if total > coupon_obj.minimum_amount:
                total -= coupon_obj.discount_price
            print('discount:',coupon_obj.discount_price)
        print('total:',total)    
        tax = (2 * total) / 100
        total += tax
        if total != 0 :
           shipping_charge = 50
        else:
             shipping_charge=0   
        print('shiping:',shipping_charge)     
        total = total + shipping_charge
    except Cart.DoesNotExist:
        pass
    if total==0:
            return redirect('shop') 
    print('-----coupon-------',coupon_obj)   
       
    context = {
        'cart': cart,
        'adresses': adresses,
        'total': total,
        'tax': tax,
        'cart_items': cart_items,
        'coupon': coupon_obj,
        'shipping_charge':shipping_charge,
        'user':user,
        'coupon':coupon_obj,
        
    }

    return render(request, 'user/checkout.html', context)
@login_required(login_url='login_user')
def addadresscheckout(request,cart_id):
    user = request.user
    addresses=Adress.objects.filter(user=user)
    
    if request.method == "POST":
        fullname = request.POST['fullname']
        phoneno = request.POST['phoneno']
        house_no = request.POST['house_no']
        street = request.POST['street']
        district = request.POST['district']
        state = request.POST['state']
        country = request.POST['country']
        postcode = request.POST['postcode']
        
       
        
        address = Adress.objects.create( 
            fullname=fullname,
            phoneno=phoneno,
            house_no=house_no,
            street=street,
            district=district,
            state=state,
            country=country, 
            postcode=postcode,
            user=user
        )
        context={
            'cart_id':cart_id
        }
        messages.success(request, f'Account Address is updated' )
        
        return redirect('checkout',cart_id)
    
    return render(request, 'user/addadresscheckout.html')