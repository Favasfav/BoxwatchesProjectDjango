from django.db import models
from django.utils.text import slugify


# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description=models.TextField(max_length=60,default=None)
    created_at=models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='products/')
    

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    Description=models.TextField(max_length=60,default=None)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    specification=models.TextField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True)
    img1=models.ImageField( upload_to='products/')
    img2=models.ImageField( upload_to='products/')
    img3=models.ImageField( upload_to='products/')
    img4=models.ImageField( upload_to='products/')
    stock=models.PositiveIntegerField()
    is_available=models.BooleanField(default=True)
    
    
    def save(self, *args, **kwargs):
             if not self.slug:
                self.slug = slugify(self.name)
             super().save(*args, **kwargs)
   
    def __str__(self):
        return self.name
class VariationManager(models.Manager):
    def colors(self):
        return super().filter(variation_category='color', is_active=True) 

    def types(self):
        return super().filter(variation_category='item_type', is_active=True)             

variation_category_choice = (
    ('color', 'Color'),
    ('item_type', 'Item Type'),
)


class ProductVariation(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='variations')
    variation_category = models.CharField(max_length=255, choices=variation_category_choice, default='color')
    variation_value = models.CharField(max_length=25, default=None)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    objects = VariationManager()

    def __str__(self):
        return self.product.name
# def offer()    