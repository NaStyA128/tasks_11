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
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)
from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse_lazy

from .models import(
    Categories,
    Products,
)
from .forms import SearchProduct


class IndexList(ListView, FormView):
    model = Products
    form_class = SearchProduct
    context_object_name = 'products'
    template_name = 'index.html'
    paginate_by = 6

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return Products.objects.filter(
                name__icontains=form.cleaned_data['name'])
        return Products.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexList, self).get_context_data(**kwargs)
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


class UpdateProduct(UpdateView):
    model = Products
    fields = ['name', 'description', 'category', 'image', 'size',
              'colour', 'price', 'quantity']
    template_name = 'add_product.html'
    success_url = '/'


class DeleteProduct(DeleteView):
    model = Products
    success_url = '/'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# class UserProfile(DetailView):
#     model = User
#     context_object_name = 'user'
#     template_name = 'profile.html'
#
#     def get_context_data(self, **kwargs):
#         print(kwargs)
#         context = super(UserProfile, self).get_context_data(**kwargs)
#         context['categories'] = Categories.objects.all()
#         return context


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


# def login(request, user):
#     user = User.objects.get(username=request.POST['username'])
#     print(user.password)
#     if user.password == request.POST['password']:
#         request.session['member_id'] = user.id
#     else:
#         return HttpResponse('Error!')


class LoginUser(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = '/'

    def form_valid(self, form):
        # self.user = form.get_user()
        # login(self.request, self.user)
        return super(LoginUser, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        # logout(request)
        return HttpResponseRedirect('/')
