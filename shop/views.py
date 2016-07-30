from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView
from django.shortcuts import get_object_or_404, get_list_or_404

from .models import(
    Categories,
    Products,
)
from .forms import SearchProduct


class CategoriesList(ListView):
    model = Categories
    context_object_name = 'categories'
    template_name = 'index.html'


class ProductsList(ListView):
    model = Products
    context_object_name = 'products'
    template_name = 'products.html'
    paginate_by = 6

    def get_queryset(self):
        # self.category = get_object_or_404(Categories, id=self.args[0])
        return Products.objects.filter(category_id=self.args[0])

    def get_context_data(self, **kwargs):
        context = super(ProductsList, self).get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        return context


class ProductDetail(DetailView):
    model = Products
    context_object_name = 'product'
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        return context


class AddProduct(CreateView):
    model = Products
    fields = ['name', 'description', 'category', 'image', 'size',
              'colour', 'price', 'quantity']
    template_name = 'add_product.html'
    success_url = '/'

