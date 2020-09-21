from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['supplier', 'text', 'department', 'amount']
        widgets = {
          'supplier': forms.Textarea(attrs={'rows':1, 'cols':100, 'style':'resize:none;'}),
          'text': forms.Textarea(attrs={'rows':15, 'cols':100}),
          'department': forms.Select(attrs={'style': 'width:183px'})
        }
