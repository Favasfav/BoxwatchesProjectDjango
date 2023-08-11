from django.urls import path
from . import views

urlpatterns = [
     
    path('', views.cart ,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:cartitem_id>/',views.remove_cart,name='remove_cart'),
    path('checkout<int:cart_id>', views.checkout, name='checkout'),
    path('reduce_quantity/<int:product_id>/', views.reduce_quantity, name='reduce_quantity'),
    path('addadresscheckout/<int:cart_id>/',views.addadresscheckout,name='addadresscheckout'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    #  path('increment_quantity/<int:product_id>/', views.increment_quantity, name='increment_quantity'),
    # path('decrement_quantity/<int:product_id>/', views.decrement_quantity, name='decrement_quantity'),
    
    
    
    
    
    
    

    
  
    
    
    
   
]