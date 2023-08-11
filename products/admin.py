from django.contrib import admin
from .models import *

# Register your models here.
class VariationAdmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value','is_active')
    list_editable=('is_active')
    list_filter=('product','variation_category','variation_value')
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductVariation)
