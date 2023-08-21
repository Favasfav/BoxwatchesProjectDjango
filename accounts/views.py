from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_control
from accounts.models import *
from django.contrib import messages
from django.core.mail import send_mail
import random
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from order.models import Order,OrderProduct
from carts.models import CartItem,Cart
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.template import Context

from io import BytesIO
from io import StringIO

from django.template.loader import get_template

import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet


from reportlab.lib import colors






# Create your views here.


def authenticate_with_email(email, password):
    User = get_user_model()
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None





@cache_control(no_cache=True,must_revalidate=True,no_store=True)  
def login_user(request):
    # if request.method=='POST':
    #     username=request.POST['username']
        
    #     Password=request.POST['password']
    #     print('dsefrfrd',Password)
    #     user=authenticate(request,username=username,password=Password)
   
    if request.method == 'POST':
        email = request.POST['email']  # Change 'username' to 'email'
        password = request.POST['password']
        user = authenticate_with_email(email, password)
        if user is not None and  user.is_active:
            login(request, user)
            return redirect('home')
        else:
            if user is not None and not user.is_active :
             messages.error (request,"User is blocked")
            else:
                 messages.error (request,"Invalid username or password") 
            return redirect('login_user')
    return render(request, 'user/Accounts/login.html')


from django.contrib import messages

@login_required(login_url='login_user')
def profile(request):
    try:
        user = request.user
        orders = Order.objects.filter(user=request.user).order_by('-created_at')

        context = {
            'user': user,
            'orders': orders,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

        return render(request, 'user/Accounts/userprofile.html', context)

    except Order.DoesNotExist:
        messages.error(request, "NO ORDER HISTORY")
        return render(request, 'user/Accounts/userprofile.html')

@login_required(login_url='login_user')
def profileorders(request):
     try:
        user = request.user
        print('user',user)
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        context = {
            'user': user,
            'orders': orders,
            
        }
        

        return render(request,'user/Accounts/profileorders.html',context)
     except Order.DoesNotExist:
        messages.error(request, "NO ORDER HISTORY")
        return render(request, 'user/Accounts/userprofile.html')
        
def generate_pdf_report(order_id,coupon_discount):
    order = Order.objects.get(id=order_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_{order_id}.pdf"'
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    content = []
    
    # Add order information
    content.append(Paragraph(f"Order ID: {order_id}", styles['Title']))
    content.append(Spacer(1, 12))
    
    content.append(Paragraph("Order Details:", styles['Heading2']))
    content.append(Paragraph(f"Created Date and Time: {order.created_at}", styles['Normal']))
    content.append(Paragraph(f"Payment Mode: {order.payment.payment_mode}", styles['Normal']))
    content.append(Paragraph(f"Delivery To: {order.address}", styles['Normal']))
    content.append(Spacer(1, 12))
    
    # Add product details
    data = [
        ["Product", "Created Date and Time", "Payment Mode", "Delivery To", "Price", "Quantity", "Total"],
    ]
    total_amount = 0
    for order_product in order.orderproduct_set.all():
        product_total = order_product.quantity * order_product.product.price
        total_amount += product_total
        data.append([
            order_product.product.name,
            order.created_at,
            order.payment.payment_mode,
            order.address,
            order_product.product.price,
            order_product.quantity,
            product_total,
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        # Add more styling options as needed
    ]))
    content.append(table)
    content.append(Spacer(1, 12))
    
    # Add order summary
    content.append(Paragraph("Order Summary:", styles['Heading2']))
    content.append(Paragraph(f"Total Amount: {total_amount}", styles['Normal']))
    if order.coupon is not None:
        coupon_discount = order.coupon.discount_price
        content.append(Paragraph(f"Coupon Discount: {coupon_discount}", styles['Normal']))
    
    tax = (2 * total_amount) / 100
    shipping_charge = 50
    grand_total = total_amount - coupon_discount + tax + shipping_charge
    
    content.append(Paragraph(f"Tax: {tax}", styles['Normal']))
    content.append(Paragraph(f"Shipping Charge: {shipping_charge}", styles['Normal']))
    content.append(Paragraph(f"Grand Total (Including Tax): {grand_total}", styles['Normal']))
    
    # Build the PDF
    doc.build(content)
    pdf = buffer.getvalue()
    buffer.close()
    
    response.write(pdf)
    return response
   
def generate_csv_report(order_id,coupon_discount):
    order = Order.objects.get(id=order_id)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="order_{order_id}.csv"'
    
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    
    # Write order information
    csv_writer.writerow(["Order ID", order_id])
    csv_writer.writerow([])
    
    csv_writer.writerow(["Order Details"])
    csv_writer.writerow(["Created Date and Time", order.created_at])
    csv_writer.writerow(["Payment Mode", order.payment.payment_mode])
    csv_writer.writerow(["Delivery To", order.address])
    csv_writer.writerow([])
    
    # Write product details header
    csv_writer.writerow(["Product", "Created Date and Time", "Payment Mode", "Delivery To", "Price", "Quantity", "Total"])
    
    total_amount = 0
    for order_product in order.orderproduct_set.all():
        product_total = order_product.quantity * order_product.product.price
        total_amount += product_total
        
        # Write product details
        csv_writer.writerow([
            order_product.product.name,
            order.created_at,
            order.payment.payment_mode,
            order.address,
            order_product.product.price,
            order_product.quantity,
            product_total,
        ])
    
    csv_writer.writerow([])
    
    # Write order summary
    csv_writer.writerow(["Order Summary"])
    csv_writer.writerow(["Total Amount", total_amount])
    if order.coupon is not None:
        coupon_discount = order.coupon.discount_price
        csv_writer.writerow(["Coupon Discount", coupon_discount])
    
    tax = (2 * total_amount) / 100
    shipping_charge = 50
    grand_total = total_amount - coupon_discount + tax + shipping_charge
    
    csv_writer.writerow(["Tax", tax])
    csv_writer.writerow(["Shipping Charge", shipping_charge])
    csv_writer.writerow(["Grand Total (Including Tax)", grand_total])
    
    response.write(csv_buffer.getvalue())
    csv_buffer.close()
    
    return response
@login_required(login_url='login_user')
def orderdetail(request,order_id):
   
        user = request.user
        order=Order.objects.get(id=order_id)
        adress=order.address
      
# Now, you can get the related OrderProduct objects using the reverse ForeignKey relationship
        order_products = order.orderproduct_set.all()
        
         
        total=0
        total1=0
        total2=0
        total3=0
        if order.coupon is not None:
            coupon_discount=order.coupon.discount_price
        else:
            coupon_discount=0   
        for order_item in order_products:
           total=order_item.sub_total
           print(total)
           total1+=total
           
           
           
           
           
        total2=total1-float(coupon_discount)

        tax=(2*total2)/100
        total2+=tax
        shipping_charge=50
        total2+=shipping_charge
        if request.method == 'POST':
           report_type = request.POST.get('report_type')
           print("-----pdf--",report_type)
           if report_type == 'pdf':
             
               return generate_pdf_report(order_id, coupon_discount)

           elif report_type == 'csv':
              return generate_csv_report( order_id,coupon_discount)

        context = {
            'user': user,
            'order': order,
            'order_products':order_products,
            'total':total,
            'total1':total1,
            'total2':total2,
            'adress':adress,
            'tax':tax,
            'coupon_discount':coupon_discount


            
        }
        

        return render(request,'user/Accounts/orderdetail.html',context)





@login_required(login_url='login_user')
def cancelorder(request,order_id):
    user=request.user
    orders=Order.objects.get(id=order_id)
    print('gdsdvscy',orders)
    orders.status = 'Cancelled'
    # order.refund_on_cancel()
    orders.save()
    user.wallet+=orders.total_price
    user.save()
    
    # To fix this, you should change OrderProduct_set to orderproduct_set. Django creates the reverse relation manager based on the lowercase model name followed by _set. 
    order_items = orders.orderproduct_set.all() 
    print('hdsfgbhd',order_items)
    
    for order_item in order_items:
        product = order_item.product
        print('Product:', product)
        print('Stock bfr:', product.stock)
        product.stock += order_item.quantity
        print('Stock aftr:', product.stock)

        product.save()
    messages.warning(request,'Order has been cancelled successfully.')     
    return redirect('profile')

    
    






@login_required(login_url='login_user') 
def changeadress(request):
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
        
        messages.success(request, f'Account Address is updated' )
  
        return render(request,'userprofile.html')
    
    return render(request, 'user/changeadress.html',{'addresses': addresses})
    

@login_required(login_url='login_user') 
def addadresscheckout(request,cart_id):
    user = request.user
    # addresses=Adress.objects.filter(user=user)
    
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
        
        messages.success(request, f'Account Address is updated' )
        
        return redirect('checkout',cart_id)

    context={

        'cart_id':cart_id
    }    
    # else:    
    #     messages.warning(request,'Not updated use any one or Add new.')
    
    #     return redirect('checkout',cart_id)
    return render(request, 'user/addadresscheckout.html',context)
    
@login_required(login_url='login_user')    
def log_out(request):
  
    logout(request)
    return redirect('home')
    
        

def signup(request):
    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        print('dsfff',get_otp)
        
        if not get_otp:
            username = request.POST['username']
            f_name = request.POST['f_name']
            l_name = request.POST['l_name']
            email = request.POST['email']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
            if UserProfile.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('signup')
            if UserProfile.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('signup')
            if pass1 != pass2:
                messages.error(request, "Passwords don't match")
                return redirect('signup')

            otp = random.randint(1000, 9999)
            
            myuser = UserProfile(username=username, email=email, first_name=f_name, last_name=l_name)
            myuser.set_password(pass1)
            print('fdfdgdf',pass1)
            myuser.verification_code = otp
            myuser.is_active=False
            print("myotp is,,,,,,",myuser.verification_code )
            myuser.save()
            

            

            mess = f'Hello {myuser.username},\nYour OTP to verify your account in Boxwatches is {otp}'
            send_mail(
                'Welcome to Boxwatches! Verify your account with your email',
                mess,
                settings.EMAIL_HOST_USER,
                [myuser.email],
                fail_silently=False
            )

            return render(request,'user/Accounts/signup.html',{'otp':True,'usr':myuser})
        
        else:
            get_email = request.POST['email']
            # print('emaul', get_email)
            user = UserProfile.objects.get(email = get_email)
            
            print('user',user.verification_code)
            if get_otp == user.verification_code:
                print('getotp/veri',get_otp ,user.verification_code)
                
                user.is_verified = True
                user.is_active= True
                
                
                user.save()
                messages.success(request,f'Account is created for {user.email}')
                return redirect(login_user)
            else:
               messages.warning(request,f'You Entered a wrong OTP')
               return render(request,'user/Accounts/signup.html',{'otp':True,'usr':user})       
    
    return render(request, 'user/Accounts/signup.html',{'otp':False})

            
    



def admin_login(request):
    if request.method == 'POST': 
        user_name = request.POST.get('username')
        password1 = request.POST.get('password')
        
        
        # Authenticate the user
        user = authenticate(username=user_name, password=password1)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('dashbord')  # Correct the URL name to 'dashboard'

        messages.error(request, "Invalid credentials")
        return redirect('admin_login')  # Correct the URL name to 'admin_login'
      
    return render(request, 'admin1/page-account-login.html') 




@login_required(login_url='login_user')
def editprofile(request):
    
    
    user = request.user
    user_profile = UserProfile.objects.get(id=user.id)
    
    context = {
        'username': user_profile.username,
        'email': user_profile.email,
        'first_name': user_profile.first_name,
        'last_name': user_profile.last_name,
         }
    
    if request.method == "POST":
       
        # ... validate and save the password change ...
          # Call the function here
        
        username = request.POST['username']
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if UserProfile.objects.filter(username=username).exists() and user_profile.username != username:
            messages.error(request, 'Username already exists')
            return redirect('editprofile')
            
        if pass1 != pass2:
            messages.error(request, "Passwords don't match")
            return redirect('editprofile')

        myuser = UserProfile(username=username, email=email, first_name=f_name, last_name=l_name)
        user_profile.username=username
        user_profile.first_name=f_name
        user_profile.last_name=l_name
        user_profile.email=email
        if pass1:
            user_profile.set_password(pass1)
            
        user_profile.save()
        messages.success(request,f'Account Details is updated for {user_profile.email}')
        return redirect('home')
        
    return render(request, 'user/editprofile.html', context)
    
@login_required(login_url='login_user')    
def addadress(request):
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
        
        messages.success(request, f'Account Address is updated' )
        
        return render(request,'user/changeadress.html',{'addresses': addresses})
    
    return render(request, 'user/addadress.html')
@login_required(login_url='login_user')    
def edit_address(request, address_id):
    
    
    address = Adress.objects.get(id=address_id)

    if request.method == 'POST':
        # Update the address fields based on the form data
        address.fullname = request.POST['fullname']
        address.phoneno = request.POST['phoneno']
        address.house_no = request.POST['house_no']
        address.street = request.POST['street']
        address.district = request.POST['district']
        address.state = request.POST['state']
        address.country = request.POST['country']
        address.postcode = request.POST['postcode']
        address.save()

        return redirect('changeadress')  # Redirect to the address list page

    return render(request, 'user/edit_address.html', {'address': address})



@login_required(login_url='login_user')
def delete_address(request, address_id):
    # Retrieve the address object based on the address_id
    address = Adress.objects.get(id=address_id)
    print(address.fullname,'dsfds')

    
    address.delete()

    return redirect('changeadress')  # Redirect to the address list page

    

 



 
    
    