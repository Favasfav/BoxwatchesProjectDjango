from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('create_order/<str:cart_id>/', views.create_order, name='create_order'),
    path('proceedtopay/',views.proceedtopay, name='proceedtopay'),
    
   
   
    # Other URL patterns
]
