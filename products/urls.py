from django.urls import path
from . import views

urlpatterns = [
    path('productlist', views.productlist, name='productlist'),
    path('categories', views.categories, name='categories'),
    path('brand', views.brand, name='brand'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('addbrand',views.addbrand,name='addbrand'),
    path('addcategory',views.addcategory,name='addcategory'),
    
    path('deletecategories/<str:name>/',views.deletecategories,name='deletecategories'),
    path('editbrand', views.editbrand, name='editbrand'),
    path('editcategory',views.editcategory,name='editcategory'),
 
    path('deletebrand/<str:name>/', views.deletebrand, name='deletebrand'),
    path('editproduct/<str:product_id>/', views.editproduct, name='editproduct'),
    path('deleteproduct/<str:name>/', views.deleteproduct, name='deleteproduct'),
   

    

    
    
]
