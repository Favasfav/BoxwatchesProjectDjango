

from django.urls import path
from . import views

urlpatterns = [
    #path('add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('addwishlist/<int:product_id>/', views.addwishlist, name='addwishlist'),
    
    
    path('remove_wishlist/<int:wishlistitem_id>/',views.remove_wishlist,name='remove_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
]
