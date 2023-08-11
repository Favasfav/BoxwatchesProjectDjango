from django.urls import path
from .import views
from adminside.views import *


urlpatterns = [
    path('dashbord', views.dashbord , name='dashbord'), 
    path('user_list', views.user_list , name='user_list'),
    path('block_unblock_user/<int:user_id>', views.block_unblock_user ,name='block_unblock_user'),
    path('orderlist', views.orderlist , name='orderlist'),
    path('sales_list', views.sales_list , name='sales_list'),
    path('orderdetails/<int:order_id>/',views.orderdetails,name='orderdetails'),
    path('update_order_status/<int:order_id>/',views.update_order_status,name='update_order_status'),
    path('cancel_order/<int:order_id>/',views.cancel_order,name='cancel_order'),
    path('coupen_list',views.coupon_list,name='coupon_list'),
    path('delete_coupon/<int:coupon_id>/',views.delete_coupon,name='delete_coupon'),
    path('add_coupon',views.add_coupon,name='add_coupon'),
       
   
]