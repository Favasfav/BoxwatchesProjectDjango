
from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Brand, Category, Product
from django.shortcuts import render
from .models import Brand
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist



def productlist(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    products = Product.objects.all()

    return render(request, 'admin1/productlist.html', {'products': products})

def categories(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    categories = Category.objects.all()
    return render(request, 'admin1/categories.html', {'categories': categories})



def brand(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    brands = Brand.objects.all()
    context = {'brands': brands}
    return render(request, 'admin1/brandlist.html', context)

from django.core.files.base import ContentFile
import base64
from PIL import Image
from io import BytesIO





import base64
import io

# def decode_cropped_img_data(cropped_img_data):
#     # Decode the base64 encoded string
#     binary_data = base64.b64decode(cropped_img_data)

#     # Convert the binary data to a PIL Image object
#     img1 = Image.open(io.BytesIO(binary_data))

#     return img1
# def decode_and_save_image(cropped_data, filename):
#     if cropped_data:
#         img_data = base64.b64decode(cropped_data)
#         img_file = ContentFile(img_data, name=filename)
#         return img_file
#     return None
import base64
from PIL import Image
from io import BytesIO

def decode_cropped_img_data(cropped_img_data, save_path='path_to_save'):
    # Remove the data:image/jpeg;base64 prefix
    image_data = cropped_img_data.split(',')[1]

    # Decode base64 data into bytes
    decoded_image_data = base64.b64decode(image_data)

    # Create a PIL Image object from the decoded bytes
    image = Image.open(BytesIO(decoded_image_data))

    # Define the save path for the image
    count=5
    #    image_filename = 'products/cropped_img{i}.jpg'
    image_filename = f'media/products/cropped_image{count}.jpg'
    count+=1
    # Rest of your code using the image_filename...

    
    # Save the image as JPEG
    image.save(image_filename, format='JPEG')

    return image_filename

from django.core.files import File
def addproduct(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    brands = Brand.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        # Extract form data
        name = request.POST['name']
        brand_id = request.POST['brand']
        category_id = request.POST['category']
        description = request.POST['description']
        specification = request.POST['specification']
        price = request.POST['price']
        cropped_img1_data = request.POST.get('cropped_img1', '')
       
        print('-----cropped_img1_data-----',cropped_img1_data)

        
        # print('-----img1-----',img1)
        # img1 = Image.open(BytesIO(image_data))
        
        # Convert the image to JPEG format
        # output = BytesIO()
        
        # print('--------img1----',img1)
        if cropped_img1_data:
           filename = decode_cropped_img_data(cropped_img1_data)
           stripped_filename = filename.replace('media/', '')
        #    filename = decode_cropped_img_data(cropped_img1_data, name, save_path='media/products')
       
        print('-----img1-----',filename )

        img2 = request.FILES['img2']
        img3 = request.FILES['img3']
        img4 = request.FILES['img4']
        stock = request.POST['stock']
        is_available = request.POST.get('is_available') == 'on'

        brand = Brand.objects.get(id=brand_id)
        category = Category.objects.get(id=category_id)

        # Check if any required field is None and show an error message
        if not name or not brand or not category or not description or not specification or not price or not img2 or not img3 or not img4 or stock is None:
            messages.error(request, "Please fill in all required fields.")
            return redirect('addproduct')

        try:
            # Try to retrieve a product with the same name
            existing_product = Product.objects.get(name=name)
            messages.error(request, f"A product with the name '{name}' already exists.")
            return redirect('addproduct')
        except ObjectDoesNotExist:
            # Product with the given name doesn't exist, proceed to add it
            product = Product(
                name=name,
                brand=brand,
                category=category,
                description=description,
                specification=specification,
                price=price,
                img1=stripped_filename,
                img2=img2,
                img3=img3,
                img4=img4,
                stock=stock,
                is_available=is_available
            )
            product.save()
            messages.success(request, 'Product added Successfully.')
            return redirect('productlist')

    context = {
        'brands': brands,
        'categories': categories,
    }
    return render(request, 'admin1/addproduct.html', context)


  



   
def addbrand(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    
    if request.method=='POST':
        
        name = request.POST['name']
        
        description = request.POST['description']
        created_at=request.POST['created_at']
        image=request.FILES['image']
        
        brand = Brand(
            name=name,
            description=description,
            image=image,
            created_at=created_at,
            
                )
        brand.save() 
        return redirect('brand') 
    return render(request, 'admin1/addbrand.html')

def addcategory(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        category = Category(
                 name=name,
                 Description=description,
            )
        category.save() 
        return redirect('categories') 
    
    return render(request, 'admin1/addcategory.html')
    
def editcategory(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    category_id = request.GET.get('category_id')
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        category = Category.objects.get(id=category_id)
        category.name = name
        category.description = description
        category.save()
        return redirect('categories')

    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return redirect('categories')

    context = {
        'category': category
    }
    return render(request, 'admin1/editcategory.html', context)

def deletecategories(request, name):
    if not request.user.is_superuser:
        return redirect('admin_login')
    try:
        category = Category.objects.get(name=name)
        category.delete()
        return redirect('categories')
    except Category.DoesNotExist:
        return redirect('categories')  # or handle the error in an appropriate way

    


def editbrand(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    brand_id = request.GET.get('brand_id')

    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        image = request.FILES['image']
        brand = Brand.objects.get(id=brand_id)
        brand.name = name
        brand.description = description
        brand.image = image
        brand.save()
        return redirect('brand')

    try:
        brand = Brand.objects.get(id=brand_id)
    except Brand.DoesNotExist:
        return redirect('brand')

    context = {
       'brand': brand
    }
    return render(request, 'admin1/editbrand.html', context)


def deletebrand(request, name):
    if not request.user.is_superuser:
        return redirect('admin_login')
    try:
        brand = Brand.objects.get(name=name)
        brand.delete()
        return redirect('brand')
    except Brand.DoesNotExist:
        return redirect('brand')  # or handle the error in an appropriate way

        
def editproduct(request, product_id):
    if not request.user.is_superuser:
        return redirect('admin_login')
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404

    brands = Brand.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        # Process the form submission
        name = request.POST['name']
        description = request.POST['description']
        image = request.FILES['image']
        brand_id = request.POST['brand']
        category_id = request.POST['category']
        specification = request.POST['specification']
        price = request.POST['price']
        stock = request.POST['stock']
        is_available = request.POST.get('is_available', False)

        brand = Brand.objects.get(id=brand_id)
        category = Category.objects.get(id=category_id)

        product.name = name
        product.description = description
        product.specification = specification
        product.price = price
        product.stock = stock
        if 'is_available' in request.POST:
              is_available = True
        else:
              is_available = False
        product.is_available = is_available

        if image:
            product.image = image

        product.brand = brand
        product.category = category

        product.save()
        return redirect('productlist')  

    context = {
        'product': product,
        'brands': brands,
        'categories': categories
    }
    return render(request, 'admin1/editproduct.html', context)

def deleteproduct(request,name):
    if not request.user.is_superuser:
        return redirect('admin_login')
    
    try:
        product = Product.objects.get(name=name)
        product.delete()
        return redirect('productlist')
    except Product.DoesNotExist:
        return redirect('productlist')