from django.db import models
from products.models import Product

from accounts.models import UserProfile
from django.conf import settings
from django.utils import timezone




class Coupons(models.Model):
    coupon_code = models.CharField(max_length=50 )
    discount_price = models.DecimalField(max_digits=5, decimal_places=2,default=100)
    is_expired = models.BooleanField(default=False)
    minimum_amount = models.IntegerField(default=500)
   
    expiry_date = models.DateField(null=True, blank=True)
    

    def __str__(self):
        return self.coupon_code
    class Meta:
        app_label = 'carts'

    

    def __str__(self):
        return self.coupon_code
           



class Cart(models.Model):
 
    cart_id = models.CharField(max_length=250, blank=True)
    coupon = models.ForeignKey(Coupons, on_delete=models.SET_NULL, null=True, blank=True)

    date_added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=None)
    is_paid = models.BooleanField(default=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    # product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.product)






    
    
    
