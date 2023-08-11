from django.db import models
from django.contrib.auth.models import AbstractUser







# Create your models here.
class UserProfile(AbstractUser):
    is_verified = models.BooleanField(blank=True, null=True)
    verification_code = models.CharField(max_length=10, blank=True, null=True)
    wallet=models.FloatField(default=0)
    
  
    
    # def add_wallet_amt(self):
    #     from order.models import *
    #     order=Order.objects.get(id)
    #     self.wallet+=self.order
         
    
    def get_wishlist_count(self):
         from wishlist.models import  WishlistItem
         return  WishlistItem.objects.filter(user=self).count()
    

    def get_cart_count(self):
     from carts.models import CartItem
     return CartItem.objects.filter(cart__is_paid=False, cart__user=self).count()


    def __str__(self):
        return str(self.email)
    
    class meta:
        db_table='userprofile'   
class Adress(models.Model):
    fullname=models.CharField(max_length=30,null=True)   
    phoneno=models.CharField(max_length=12,null=True)
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    house_no=models.CharField(max_length=20)
    street=models.CharField(max_length=20)
    district=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    country=models.CharField(max_length=20)
    postcode=models.IntegerField()
    
    
    def __str__(self):
         return f"{self.house_no}, {self.street}, {self.district}, {self.postcode}"

    
    
         
         


    