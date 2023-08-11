from django.contrib import admin
from .models import Cart,CartItem,Coupons

# # Register your models here.


admin.site.register(Coupons)
admin.site.register(CartItem)
admin.site.register(Cart)


