from django.shortcuts import render
from products.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout




# Create your views here.
 
def index(request):
    products = Product.objects.all().order_by('-created_at')[:6] 
    print('Request GET parameters:', request.GET)
    categories = Category.objects.all()
    brands = Brand.objects.all()
    print('-----categories----',categories)
    sort_by = request.GET.get('sort')
    print('Sort by:', sort_by)
    selected_category_id = request.GET.get('category')
    selected_brand_id = request.GET.get('brand')   # Get the selected category ID
    # li=["static/user/assets/img/gallery/1828KM02_1.webp","static/user/assets/img/gallery/5303R_001_11@2x.jpg","static/user/assets/img/gallery/2652NM01_1 (1).webp"]
    
    
    
    return render(request,'user/index.html',{'products':products,'categories':categories,'brands':brands})

    
def about(request):
    return render(request,'user/about.html')   
def contact(request):
    return render(request,'user/contact.html')        


def shop(request):
    products = Product.objects.all()
    print('Request GET parameters:', request.GET)
    categories = Category.objects.all()
    brands = Brand.objects.all()
    print('-----categories----',categories)
    sort_by = request.GET.get('sort')
    print('Sort by:', sort_by)
    selected_category_id = request.GET.get('category')
    selected_brand_id = request.GET.get('brand')   # Get the selected category ID

    if selected_category_id:  # If a category is selected
        products = products.filter(category_id=selected_category_id)
    if selected_brand_id:  # If a category is selected
        products = products.filter(brand_id=selected_brand_id)    

    if sort_by == 'price_high_to_low':
        products = products.order_by('-price')
        print('------ products-----', products)
    elif sort_by == 'low_to_high':
        products = products.order_by('price')
    elif sort_by=='below_5000':
        products=products.filter(price__lte=5000)    
    else:
        pass    
    
    return render(request,'user/shop.html',{'products':products,'categories':categories,'brands':brands})

def product_details(request,product_id):
    products = Product.objects.get(id=product_id)
    
    return render(request,'user/product_details.html',{'product':products})
    

    

    