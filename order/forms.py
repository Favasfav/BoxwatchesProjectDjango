from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'payment', 'order_number', 'order_note', 'order_total', 'tax', 'status', 'address', 'total_price', 'ip', 'is_ordered']
