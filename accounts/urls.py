from django.urls import path
from . import views

urlpatterns = [
     
    path('login_user', views.login_user ,name='login_user'),
    path('signup', views.signup ,name='signup'),
    path('admin_login',views.admin_login,name='admin_login'),
    path('profile',views.profile,name='profile'),
    path('logout',views.log_out,name='logout'),
    path('changeadress',views.changeadress,name='changeadress'),
    path('addadress',views.addadress,name='addadress'),
    path('editprofile',views.editprofile,name='editprofile'),
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('cancelorder/<int:order_id>/', views.cancelorder, name='cancelorder'),
     path('profileorders',views.profileorders,name='profileorders'),
    path('orderdetail/<order_id>/',views.orderdetail,name='orderdetail'), 
    path('addadresscheckout/<cart_id>/',views.addadresscheckout,name='addadresscheckout'), 
    


    
    
    
   
]