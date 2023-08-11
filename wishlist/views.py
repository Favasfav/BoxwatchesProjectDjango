
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from accounts.models import *
from products.models import *
from carts.models import *
from .models import WishlistItem  # Use relative import
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Rest of your code ...



@login_required(login_url='login_user')
def wishlist(request):
    
    user = request.user
    
         
    wishlist_items = WishlistItem.objects.filter(user=user)
    if not wishlist_items:
        messages.error(request, 'No item found in wishlist')
        return redirect('shop')
    else:    
        
        return render(request, 'user/wishlist.html', {'wishlist_items': wishlist_items})
@login_required(login_url='login_user')
def addwishlist(request,product_id):
    if request.method=='POST':
        print("fdsg",product_id)
        product=Product.objects.get(id=product_id)
        print('prdct',product.name)
        wishlist, created =WishlistItem.objects.get_or_create(user=request.user, product=product)

        if created:
            messages.success(request,'Product added to Wishlist.')
            return redirect('wishlist')
        else:
            messages.warning(request,'Product already in wishlist.')
            return redirect('wishlist')
    
from django.shortcuts import get_object_or_404
@login_required(login_url='login_user')
def remove_wishlist(request, wishlistitem_id):
    try:
        wishlistItem = get_object_or_404(WishlistItem, id=wishlistitem_id)
        wishlistItem.delete()
        messages.success(request, 'Item removed from wishlist')
    except WishlistItem.DoesNotExist:
        messages.error(request, 'Item not found in wishlist')
    
    return redirect('wishlist')


