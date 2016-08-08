from django import forms
from django.forms import MultiWidget
from django.contrib.auth.forms import UserCreationForm

from .models import Products, Buyers,  MyUsers

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


class PhoneWidget(MultiWidget):

    def __init__(self, code_l, n_l, attrs=None, *args, **kwargs):
        widgets = [forms.TextInput(attrs={'size': code_l, 'maxlength': code_l}),
                   forms.TextInput(attrs={'size': n_l, 'maxlength': n_l}),]
        super(PhoneWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.code, value.number]
        return ['', '']

    def format_output(self, rendered_widgets):
        return "+38("+rendered_widgets[0]+')'+rendered_widgets[1]


class PhoneField(forms.MultiValueField):

    def __init__(self, code_l, n_l, *args, **kwargs):
        list_fields = [forms.CharField(), forms.CharField()]
        super(PhoneField, self).__init__(list_fields, widget=PhoneWidget(code_l, n_l), *args, **kwargs)

    def compress(self, values):
        return "+38"+values[0]+values[1]


# class BuyersForm(forms.ModelForm):
#     class Meta:
#         model = Buyers
#         fields = ['name', 'phone']


class RegistrationForm(UserCreationForm):
    phone = PhoneField(3, 7)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            MyUsers.objects.create(user=user, phone=self.cleaned_data["phone"])
        return user


class BuyersForm2(forms.Form):
    name = forms.CharField(max_length=100)
    phone = PhoneField(3, 7)

    # class Meta:
    #     model = Buyers
    #     fields = ['__all__']
    #     widgets = {'name': forms....}
