from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, get_list_or_404

from .models import(
    Categories,
    Products,
)


class CategoriesList(ListView):
    model = Categories
    context_object_name = 'categories'
    template_name = 'index.html'


class ProductsList(ListView):
    model = Products
    context_object_name = 'products'
    template_name = 'products.html'
    paginate_by = 5

    def get_queryset(self):
        # self.category = get_object_or_404(Categories, id=self.args[0])
        return Products.objects.filter(category_id=self.args[0])

    # def get_context_data(self, **kwargs):
    #     context = super(ProductsList, self).get_context_data(**kwargs)
    #     context['category'] = self.category
    #     return context


class ProductDetail(DetailView):
    model = Products
    context_object_name = 'product'
    template_name = 'product.html'
