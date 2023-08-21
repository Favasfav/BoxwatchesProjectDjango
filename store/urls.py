from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
     
    path('', views.index,name='home'),
    path('shop', views.shop,name='shop'),
    path('product_details <int:product_id>',views.product_details,name='product_details'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    

    
    
   
]
