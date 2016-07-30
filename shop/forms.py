from django import forms

from .models import Products


class SearchProduct(forms.ModelForm):
    class Meta:
        model = Products
        fields = [
            'name',
        ]
