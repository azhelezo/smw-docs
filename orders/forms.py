from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['text', 'amount']
        widgets = {
          'text': forms.Textarea(attrs={'rows':20, 'cols':100}),
        }
