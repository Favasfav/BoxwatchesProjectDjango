

# # Create your models here.
# # models.py
from django.db import models
from django.contrib.auth.models import User
from accounts.models import *
from products.models import * 
from carts.models import *

class WishlistItem(models.Model):
     user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
     product= models.ForeignKey(Product, on_delete=models.CASCADE)
     added_date = models.DateTimeField(auto_now_add=True)

     def __str__(self):
       return self.product
