from django.shortcuts import render, redirect,HttpResponse
from carts.models import CartItem,Cart,Coupons
from accounts.models import Adress,UserProfile
import datetime
from .models import Order, OrderProduct,Payment
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
from decimal import Decimal

@login_required(login_url='login_user')
def create_order(request,cart_id):
    print('hai')
    user=request.user
    
    print('user1111',user) 
    print('cart_id',cart_id)
    
    
    if request.method =='POST':   
        cart = Cart.objects.filter(id=cart_id)
        # if if 'form1' in request.POST:
        coupon_code = request.POST.get('coupon')
        # coupon_code = request.POST.get('coupon_code')
        print('-----coupon_code---',coupon_code)
        try:
        # Attempt to fetch the coupon object based on the provided code
            coupon_obj = Coupons.objects.get(coupon_code__iexact=coupon_code)
        except Coupons.DoesNotExist:
        # Handle the case when the coupon with the provided code does not exist
            coupon_obj = None 
        print('coupon-------------',coupon_obj)    
        for i in cart:
             x=i.user_id
        print("fdgr",cart)
        user=x
        
        # print('fdg',cart)
        # print('ghc',user)
        cart_items = CartItem.objects.filter(cart__user=user)
        print('Cart Items:', cart_items)    
        adress_id = request.POST.get('billing_address')
        print('Selected Address ID:', adress_id)
        adress = Adress.objects.get(id=adress_id)
          
    
        print('gfsga',adress)
    
        
        
        # cart_count = cart_items.count()
        # if cart_count <= 0:
        #          return redirect('cart')
        total=0
        grand_total = 0
        tax = 0
        total1=0
        try:
            cart1 = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            return HttpResponse("Cart does not exist.")
        coupon_obj = cart1.coupon
        # print('gfchgc',coupon_obj)

        for cart_item in cart_items:
               total = (cart_item.product.price * cart_item.quantity)
               grand_total += total
               cart_item.product.stock-=cart_item.quantity
               
               cart_item.product.save()     
               
              
        total_before=grand_total      
              
        if coupon_obj:
            if grand_total > coupon_obj.minimum_amount:
                
                grand_total -= coupon_obj.discount_price  
                       
              
        print(' grnd totl :',grand_total)         
        tax = (2 * grand_total) / 100
        grand_total += tax
       
        print(" auth  ",request.user.is_authenticated)
        user2 = UserProfile.objects.get(id=user)

        print('user:',user2)
        adresses = Adress.objects.filter(user=user)
        
        if grand_total != 0 :
           shipping_charge = 50
        else:
             shipping_charge=0   
            
        grand_total = grand_total + shipping_charge
        payment_mode = request.POST.get('payment_mode')
        print('-------payment_mode----',payment_mode)
        if payment_mode =='Wallet' or payment_mode == 'Razorpay':
            pass
        else:
            payment_mode='COD'    
            
        print('-------payment_mode----',payment_mode)
        if payment_mode == 'Wallet':
            wallet_balance = user2.wallet
            if grand_total <= wallet_balance:
                payment_mode = 'Wallet'
                wallet_balance -= float(grand_total)
                user2.wallet = wallet_balance
                user2.save()  
            else:
                messages.error(request, "Insufficient wallet balance.")
                return redirect('checkout')  
              
        
         
        
        print('------payment mode---->',payment_mode)
        payment_id = None
       
        if payment_mode == 'Razorpay':
            payment_id = request.POST.get('payment_id')
            # print('------------------------------>>>>>>',payment_id)
        elif payment_mode == 'COD':
            payment_id = None

        if payment_mode:
            # Create payment object for both online payment methods and COD
            payment = Payment.objects.create(
                user=user2,
                payment_id=payment_id,
                payment_mode=payment_mode,
                amount_paid=grand_total,
                status='new'
            )
            # Save the payment object to the database
            payment.save()
        try:
        # Attempt to fetch the selected address based on the provided ID
             adress_id = request.POST.get('billing_address')
             if not adress_id:
                 messages.error(request, "Please select a billing address.")
                 return redirect('addadress')  # Redirect to an appropriate page

             address = Adress.objects.get(id=adress_id)
        except Adress.DoesNotExist:
           messages.error(request, "Selected address does not exist.")
           return redirect('addadress')  # Redirect to an appropriate page    
        # print('-------------------payment---->',payment)
            
        # adress_instance = Adress.objects.get(id=adress)
       
            # Attempt to create an order object
        order = Order.objects.create(
                user=user2,
                address=address,
                order_total=grand_total,
                tax=tax,
                status='New',
                total_price=grand_total,
                coupon=coupon_obj,
            )
        
        

        if payment:
            order.payment = payment
            order.save()
            print('-------------------order---->',order)
        for cart_item in cart_items:

                # product_variation = cart_item.product_variation
                print('-------------------------cattitem',cart_item.product)
               
                sub_total = int(cart_item.quantity*cart_item.product.price)
                order_product = OrderProduct.objects.create(
                             order=order,
                             product=cart_item.product,
                             user=user2,
                             payment=payment,
                             color="",
                             item_type="",
                             poduct_price=cart_item.product.price,
                             quantity=cart_item.quantity,
                             sub_total = sub_total

                            #  variation_id=product_variation.id,
                         )
        print('------------------------- order_product', order_product)
            #         # Clear the cart
        # cart_items.delete()
        cart1.delete()
            #  # Generate order number and set it to order.order_number
            #         # You can use any logic to generate the order number
        yr = datetime.date.today().strftime('%y')
        dt = datetime.date.today().strftime('%d')
        mt = datetime.date.today().strftime('%m')
        current_date = yr + mt + dt
        order_number = current_date + str(order.id)
        order.order_number = order_number
        created_at=order.created_at
        order.save()
        print('-------------------order---->',order)
        subtotal=0
        order_items = order.orderproduct_set.all() 
        
        context = {
                 'adress': adress,
                 'grand_total': grand_total,
                 'tax': tax,
                 'order_number': order_number,
                 'total1':total1,
                 'created_at':created_at,
                 'order_items':order_items,
                 'payment_id':payment_id,
                 'payment_mode':payment_mode,
                 'order':order,
                 'total':total,
                 'total_before':total_before,
                 
                 
             }
        print('context',context)  
          

    
    payMode = request.POST.get('payment_mode')
    print('paymode',payMode)
    if (payMode == "Razorpay"):
        return JsonResponse({'status':"Your order has been placed successfully."})
        
            
    return render(request, 'user/confirmation.html',context)
    
    
@login_required(login_url='login_user')   
def proceedtopay(request):
        
        user=request.user
        try:
             
           cart = Cart.objects.filter(user=request.user).first()
               
        except Cart.DoesNotExist:
            return HttpResponse("Cart does not exist.")
        if request.method == 'POST':
            coupon_code = request.POST.get('coupon')
            print('--------coupon_code----',coupon_code)    

        # for i in cart:
        #      x=i.user_id
        #      print(i)
        # print("fdgr",cart)
        # user=x
        
        # print('fdg',cart)
        # print('ghc',user)
        cart_items = CartItem.objects.filter(cart__user=user)
        print('Cart Items:', cart_items)
        
        # cart_count = cart_items.count()
        # if cart_count <= 0:
        #          return redirect('cart')
        total=0
        grand_total = 0
        tax = 0
      

        for cart_item in cart_items:
               total = (cart_item.product.price * cart_item.quantity)
               
               
               grand_total += total
               
               
        try:
        # Attempt to fetch the coupon object based on the provided code
            coupon_obj = Coupons.objects.get(coupon_code__iexact=coupon_code)
        except Coupons.DoesNotExist:
        # Handle the case when the coupon with the provided code does not exist
            coupon_obj = None       
              
        # print('total1 in aftr shiping:',total1)      
        if coupon_obj:
            if grand_total > coupon_obj.minimum_amount:
                
                grand_total -= coupon_obj.discount_price        
        # if coupon_obj:
        #     if total > coupon_obj.minimum_amount:
        #         grand_total -= coupon_obj.discount_price         
               
        tax = (2 * grand_total) / 100
        grand_total += tax
        
       
        

        # print('user:',user2)
        # adresses = Adress.objects.filter(user=user)
        
        if grand_total != 0 :
           shipping_charge = 50
        else:
             shipping_charge=0   
        print('shiping:',shipping_charge)     
        total1 = grand_total + shipping_charge
        print("total1:",total1)
        return JsonResponse({'status': 'Not allowed this Quantity','total1':total1})

           

        
        
