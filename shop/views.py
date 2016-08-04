from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)
from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse

from .models import(
    Categories,
    Products,
    Buyers
)
from .forms import SearchProduct, BuyersForm2


class IndexList(ListView, FormView):
    model = Products
    form_class = SearchProduct
    context_object_name = 'products'
    template_name = 'index.html'
    paginate_by = 6

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        form.is_valid()
        if self.request.GET:
            if self.request.GET['name'] and self.request.GET['ordering']:
                q = Products.objects.filter(
                    name__icontains=form.cleaned_data['name']).order_by(
                    form.cleaned_data['ordering'])
            elif self.request.GET['ordering']:
                q = Products.objects.all().order_by(
                    form.cleaned_data['ordering'])
            else:
                q = Products.objects.filter(
                    name__icontains=form.cleaned_data['name'])
            return q
        return Products.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexList, self).get_context_data(**kwargs)
        if self.request.GET.get('name'):
            context['search_name'] = self.request.GET.get('name')
        if self.request.GET.get('ordering'):
            context['search_ordering'] = self.request.GET.get('ordering')
        context['categories'] = Categories.objects.all()
        return context


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

    def get_context_data(self, **kwargs):
        context = super(AddProduct, self).get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        return context

    def get_success_url(self):
        return reverse('products-list', args={self.object.category_id})

    # def get(self, request, *args, **kwargs):
    #     # ?rediret_uri=sdfsdfs
    #     # self.success_url = '/%s/' % request.GET.get('redirect_uri')
    #     # print(self.success_url)
    #     self.object = None
    #     response = super(AddProduct, self).get(request, *args, **kwargs)
    #     return response


class UpdateProduct(UpdateView):
    model = Products
    fields = ['name', 'description', 'category', 'image', 'size',
              'colour', 'price', 'quantity']
    template_name = 'add_product.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(UpdateProduct, self).get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        return context

    def get_success_url(self):
        return reverse('products-list', args={self.object.category_id})


class DeleteProduct(DeleteView):
    model = Products

    def get_success_url(self):
        return reverse('products-list', args={self.object.category_id})

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class UserProfile(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        return context


class RegistrationUser(FormView):
    form_class = UserCreationForm
    template_name = 'add_user.html'
    success_url = 'login/'

    def form_valid(self, form):
        form.save()
        return super(RegistrationUser, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RegistrationUser, self).get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        return context


class LoginUser(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = '/'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginUser, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LoginUser, self).get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        return context


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class BuyersView(FormView):
    form_class = BuyersForm2
    template_name = 'buyers.html'
    success_url = '/'
