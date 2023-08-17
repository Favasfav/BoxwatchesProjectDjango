from django.shortcuts import render,redirect
from accounts.models import UserProfile
from order.models import Order, OrderProduct
from products.models import *
from django.contrib import messages
from carts.models import Cart, Coupons
from django.db.models import Sum
import datetime
from django.utils import timezone
from datetime import timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import csv
from django.http import HttpResponse
from django.db.models import Count
from datetime import datetime, timedelta
from django.contrib.auth import update_session_auth_hash





def dashbord(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
       
    
    # total_count_order=Order.objects.count()
    shiping_charge=50
    # total_revenue = Order.objects.aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0
    # total_revenue -= (Order.objects.count() * shiping_charge)  
    # total_revenue_formatted = '{:.2f}'.format(total_revenue)   
    accepted_orders = Order.objects.filter(status='Accepted')
    accepted_orders_count = Order.objects.filter(status='Accepted').count()
    total_accepted_revenue = accepted_orders.aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0
    total_accepted_revenue -=(accepted_orders_count*shiping_charge)
    total_accepted_revenue = '{:.2f}'.format(total_accepted_revenue)

    total_products_order=Order.objects.count()
    total_unique_products = OrderProduct.objects.values('product').distinct().count()


    total_products_categories = OrderProduct.objects.values('product__category').distinct().count()

    today=timezone.now()  
    this_month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    total_revenue_thismonth = Order.objects.filter(created_at__gte=this_month_start,status='Accepted').aggregate(
        total_revenue_month=Sum('total_price'))['total_revenue_month'] or 0
      
    
    today = timezone.now()
    start_of_week = today - timedelta(days=6)
    end_of_today = today.replace(hour=23, minute=59, second=59, microsecond=999999)
    weekly_sales = Order.objects.filter(
    created_at__gte=start_of_week,
    created_at__lte=end_of_today,
    status='Accepted').aggregate(total_revenue_week=Sum('total_price'))['total_revenue_week'] or 0
    weekly_sales_count = Order.objects.filter(
    created_at__gte=start_of_week,
    created_at__lte=end_of_today,
    status='Accepted').count()
    weekly_sales-=(weekly_sales_count*shiping_charge)
    start_of_today = today.replace(hour=0, minute=0, second=0)

    today_sales=Order.objects.filter(created_at__gte=start_of_today,status='Accepted').aggregate(total_revenue_today=Sum('total_price'))['total_revenue_today'] or 0    
    today_sales_count=Order.objects.filter(created_at__gte=start_of_today,status='Accepted').count()
    today_sales-=(today_sales_count*shiping_charge)
    weekly_sales_formatted = '{:.2f}'.format(weekly_sales) 


    orders = Order.objects.all().order_by('-created_at')
    products = Product.objects.all().order_by('created_at')

    # Calculate the last 6 months from the current date
    
    last_six_months = [today.strftime('%B')]  # Initialize the list with the current month
    for i in range(1, 6):
        previous_month = today - timedelta(days=30*i)
        last_six_months.append(previous_month.strftime('%B'))
    # Calculate total sales for each of the last six months
    total_sales_data = []
    for i in range(6):
        start_date = today - timedelta(days=30*(i+1))
        end_date = today - timedelta(days=30*i)
        total_sales = Order.objects.filter(created_at__gte=start_date, created_at__lt=end_date,status='Accepted').count()
        total_sales_data.append(total_sales)
    

    total_visitors_data = []
    for i in range(6):
        start_date = today - timedelta(days=30*(i+1))
        end_date = today - timedelta(days=30*i)
        total_visitors = UserProfile.objects.filter(date_joined__gte=start_date, date_joined__lt=end_date).count()
        total_visitors_data.append(total_visitors) 

    categories = Category.objects.all() 
    
    # Calculate the sales for each category
    category_sales_data = []
    category_names = []
    for category in categories:
        category_names.append(category.name)
        total_sales = OrderProduct.objects.filter(product__category=category, order__status='Completed').aggregate(total_sales=Sum('quantity'))['total_sales'] or 0
        category_sales_data.append(total_sales)
    # Perform the query to get payment mode counts
    payment_mode_counts = Order.objects.exclude(payment__payment_mode=None).values('payment__payment_mode').annotate(order_count=Count('order_number'))
      # Extract labels and data for the transaction chart.
    labels = [item['payment__payment_mode'] for item in payment_mode_counts]
    data = [item['order_count'] for item in payment_mode_counts]  

    # Query to get the count of orders for each order status
    order_status_counts = Order.objects.values('status').annotate(order_count=Count('status'))
    
    # Extract labels and data for the chart
    order_labels = [item['status'] for item in order_status_counts]
    order_data = [item['order_count'] for item in order_status_counts]

    # print('-----order_labels,order_data---------',order_data,order_labels)
    order=Order.objects.all()               


    
    context={
        'total_accepted_revenue':total_accepted_revenue,
        
        'total_products_order':total_products_order,
       
        'total_unique_products': total_unique_products,
        'total_products_categories':total_products_categories,
        'total_revenue_thismonth': total_revenue_thismonth,
        'today_sales':today_sales,
        'weekly_sales':weekly_sales_formatted,
        'orders':orders,
        'products':products,
        'last_six_months': last_six_months,
        'total_sales_data': total_sales_data,
        'total_visitors_data': total_visitors_data,
        'category_sales_data':category_sales_data,
        'data':data,
        'labels':labels,
        'order':order,
        
    }
    return render(request,'admin1/dashbord.html',context)


def sales_list(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
   
    start_date = None
    end_date = None
    sales_lists = None
    
    
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        report_type = request.POST.get('report_type')
        print('ghsdcs')
        
        try:
            if start_date_str:
               start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            if end_date_str:
               end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
               end_date += timedelta(days=1)  # Add one day to include the entire last day
               end_date -= timedelta(seconds=1)
            print('strtdate',start_date,'end_date',end_date)
            if start_date and end_date:
                sales_lists = Order.objects.filter(created_at__range=[start_date, end_date],status='Accepted')
            elif not start_date and not end_date:
                sales_lists = Order.objects.filter(status='Accepted') 
            print('---------saleslidt',sales_lists)    
            
            if report_type == 'pdf':
                return generate_pdf_report(sales_lists)
            elif report_type == 'csv':
                return generate_csv_report(sales_lists)
        except ValueError:
            error_message = "Invalid date format. Please use YYYY-MM-DD."
            return render(request, 'admin1/saleslist.html', {'error_message': error_message})
    else:
        sales_lists = Order.objects.filter(status='Accepted') 
    return render(request, 'admin1/saleslist.html', {'sales_lists': sales_lists})



from reportlab.platypus import Table, TableStyle

def generate_pdf_report(sales_lists):
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("Sales Report", styles['Title']))
    content.append(Paragraph("Generated by BoxWatches", styles['Normal']))

    # Create a table for the report content
    data = [['Order Number','Customer', 'Created At', 'Total']]
    for sale in sales_lists:
        data.append([sale.order_number,sale.user.username, sale.created_at, sale.order_total])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#007bff'),
        ('TEXTCOLOR', (0, 0), (-1, 0), '#FFFFFF'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), '#e6e6e6'),
        ('GRID', (0, 0), (-1, -1), 1, '#FFFFFF'),
    ]))
    
    content.append(table)
    doc.build(content)
    
    return response
import csv

def generate_csv_report(sales_lists):
   
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

    writer = csv.writer(response)
    
    # Write CSV header
    writer.writerow(['Order Number','Customer', 'Created At', 'Total'])
    
    # Write data rows
    for sale in sales_lists:
        writer.writerow([sale.order_number,sale.user.username, sale.created_at, sale.order_total])

    return response



# Create your views here.
def user_list(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    users=UserProfile.objects.all()
    # for i in users:
    #       print("gggggg",i.is_blocked)
    return render(request,'admin1/user_list.html',{'users': users})


def block_unblock_user(request,user_id):
    if not request.user.is_superuser:
        return redirect('admin_login')
    
    user = UserProfile.objects.get(id=user_id)
  
    
    if user.is_active:
          user.is_active = False
          user.save()
    else:
        user.is_active = True
        user.save()
    
        
    return redirect('user_list')

def orderlist(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    orders = Order.objects.all().order_by('-created_at')

   
    return render(request,'admin1/orderlist.html',{'orders': orders})
    

def cancel_order(request,order_id):
    if not request.user.is_superuser:
        return redirect('admin_login')
    order = Order.objects.get(id=order_id)

     # Update the order status to "Cancelled"
    order.status = 'Cancelled'
    order.save()

    # Increase the product stock for each order item
    order_items = order.orderproduct_set.all()
    for order_item in order_items:
        product = order_item.product
        product.stock += order_item.quantity
        product.save()

    messages.warning(request,'Order has been cancelled successfully.')

    return redirect('orderlist')
def orderdetails(request,order_id):
    if not request.user.is_superuser:
        return redirect('admin_login')
    order=Order.objects.get(id=order_id)
    print('gdsdvscy',order)
    
    # To fix this, you should change OrderProduct_set to orderproduct_set. Django creates the reverse relation manager based on the lowercase model name followed by _set. 
    order_items = order.orderproduct_set.all() 
    total=0
    li=[]
    total1=0
    for order_item in order_items:
        # order_item.sub_total=order_item.sub_total()
        total=order_item.poduct_price*order_item.quantity
        li.append(total)
        total1+=total

    if total1!=0:    
        deliverycharge =50  
    else:
        deliverycharge =0    
    total1+=order.tax+deliverycharge 

    print(li)
    context = {
        'order': order,
        'order_items': order_items,
        'total':total,
        'STATUS':Order.STATUS,
        'li':li,
        'total1':total1,
    }
    
    return render(request, 'admin1/orderdetails.html', context)
def update_order_status(request, order_id):
    if not request.user.is_superuser:
        return redirect('admin_login')
    order = Order.objects.get(id=order_id) 

    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        order.status = new_status
        order.save()
        messages.warning(request,'Order status has been changed successfully.')
   
    return redirect('orderlist')
def coupon_list(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    coupons = Coupons.objects.all()
    context = {
        'coupons': coupons
    }
    return render(request, 'admin1/coupon_list.html', context)
def delete_coupon(request,coupon_id):
    if not request.user.is_superuser:
        return redirect('admin_login')
    coupon_obj=Coupons.objects.get(id=coupon_id)
    
    coupon_obj.delete()
    return redirect('coupon_list')
def add_coupon(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    if request.method == 'POST':
            # Get the expiry date from the form data
                coupon_code = request.POST.get('coupon_code')
                discount_price = request.POST.get('discount_price')
                is_expired = request.POST.get('is_expired')
                minimum_amount=request.POST.get('minimum_amount')

        
                

            # Now you can use the expiry_date as a Python date object and save it to the model
            # For example, assuming you have a model called Coupons:
                coupon = Coupons.objects.create(
                coupon_code=request.POST['coupon_code'],
                discount_price=request.POST['discount_price'],
                is_expired=request.POST.get('is_expired', False),
                
                 minimum_amount= minimum_amount
                 )
            # Save the coupon to the database
                coupon.save()
                messages.warning(request,'Coupon has been created successfully.')
                return redirect('coupon_list')

    return render(request,'admin1/addcoupon.html')




    

