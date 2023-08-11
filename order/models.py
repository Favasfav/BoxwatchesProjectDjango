from django.db import models
from products.models import Product
from accounts.models import UserProfile
from accounts.models import Adress
from products.models import ProductVariation
from carts.models import Coupons

class Payment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=250, null=True)
    payment_mode = models.CharField(max_length=150)
    amount_paid = models.CharField(max_length=150 )
    status=models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_id
    
    
    



class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('pending','pending'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
        
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,blank=True,null=True)
    order_number=models.CharField(max_length=34)
    order_note=models.CharField(max_length=34,blank=True)
    order_total=models.FloatField()
    tax=models.FloatField()
    status=models.CharField(max_length=34,blank=True,choices=STATUS)
    address = models.ForeignKey(Adress, on_delete=models.CASCADE)
    total_price = models.FloatField(null=False,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupons, on_delete=models.SET_NULL, null=True, blank=True)

    
   
    

    def __str__(self):
        return f"{self.id, self.order_number}"
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,blank=True,null=True)
    # variation=models.ForeignKey(ProductVariation,on_delete=models.CASCADE)
    color=models.CharField(max_length=33)
    item_type=models.CharField(max_length=33) 
    poduct_price= models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    sub_total= models.FloatField(null=False)
    
    
   
    
    orderstatuses = {
        ('Pending','Pending'),
        ('Processing','Processing'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Return', 'Return')
    }
    status = models.CharField(max_length=150,choices=orderstatuses, default='Pending')
    def calculate_sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.order.id}"
         
    