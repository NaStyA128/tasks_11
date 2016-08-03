from django import forms

from .models import Products

CHOICES = (('name', 'name'), ('price', 'price'))


class SearchProduct(forms.ModelForm):
    ordering = forms.ChoiceField(choices=CHOICES, required=False)
    name = forms.CharField(
        max_length=100,
        required=False
    )

    class Meta:
        model = Products
        fields = [
            'name',
        ]
