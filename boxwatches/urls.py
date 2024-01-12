from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.defaults import page_not_found


urlpatterns = [
    path('', include('adminside.urls')),
    path('admin/',admin.site.urls),
    path('', include('store.urls')),
    path('', include('accounts.urls')),
 
    path('', include('products.urls')),
    path('cart/',include('carts.urls')),
    path('order/',include('order.urls')),
    path('wishlist/',include('wishlist.urls')),
    
    
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'products.views.custom_404_page'