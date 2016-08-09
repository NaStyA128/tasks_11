import json

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
from django.contrib.sessions.models import Session

from .models import(
    Categories,
    Products,
    MyUsers,
    Orders,
    OrderProducts
)
from .forms import SearchProduct, BuyersForm2, RegistrationForm


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

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            u = MyUsers.objects.get(user_id=request.user.id)
            self.user_id = u.id
        else:
            self.user_id = None
        return super(UserProfile, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        if self.user_id:
            context['user_all_info'] = MyUsers.objects.get(id=self.user_id)
            list_orders = Orders.objects.filter(user_id=self.user_id).all()
            list_products_in_orders = []
            for order in list_orders:
                list_products_in_orders.append(
                    OrderProducts.objects.filter(order_id=order.id).all()
                )
            context['orders'] = list_orders
            context['products_orders'] = list_products_in_orders
            return context


class RegistrationUser(FormView):
    form_class = RegistrationForm
    template_name = 'add_user.html'
    success_url = 'login/'

    # def save(self, commit=True):
    #     user = super(UserCreationForm, self).save(commit=False)
    #     return super(RegistrationUser, self).save(commit)

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


class CartView(TemplateView):
    template_name = "cart.html"

    def post(self, request, *args, **kwargs):
        my_lists = request.session.get('cart', False)
        for product in my_lists:
            if int(request.POST.get('product_id', False)) == int(product.id):
                this_product = Products.objects.get(
                    id=int(request.POST.get('product_id', False))
                )
                request.session['total_cart'] -= product.price
                price = this_product.price * int(
                    request.POST.get('new_quantity', False))
                product.price = price
                if product.quantity_in_cart < product.quantity:
                    product.quantity_in_cart = int(request.POST.get(
                        'new_quantity', False))
                request.session['total_cart'] += product.price
        request.session['cart'] = my_lists
        return HttpResponseRedirect('/cart/')

    def get(self, request, *args, **kwargs):
        if not request.session.get('cart', False):
            request.session['cart'] = list()
            request.session['total_cart'] = 0
        if request.GET.get('product', False):
            my_lists = request.session.get('cart', False)
            # if my_lists:
            #     for product_in_cart in my_lists:
            #         if product_in_cart.id == int(request.GET.get('product', False)):
            #             product_in_cart.quantity_in_cart += 1
            product = Products.objects.get(
                id=int(request.GET.get('product', False))
            )
            product.quantity_in_cart = 1
            my_lists.append(product)
            request.session['cart'] = my_lists
            request.session['total_cart'] += product.price
            return HttpResponseRedirect('/cart/')
        if request.GET.get('delete', False):
            my_lists = request.session.get('cart', False)
            for prod in my_lists:
                if prod.id == int(request.GET.get('delete', False)):
                    request.session['total_cart'] -= prod.price
                    my_lists.remove(prod)
                    request.session['cart'] = my_lists
            return HttpResponseRedirect('/cart/')
        return super(CartView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        return context


class MakeOrderView(TemplateView):
    template_name = "make_order.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            u = MyUsers.objects.get(user_id=request.user.id)
            self.user_id = u.id
        else:
            self.user_id = None
        return super(MakeOrderView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MakeOrderView, self).get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        if self.user_id:
            context['user_all_info'] = MyUsers.objects.get(id=self.user_id)
        return context


class CreateOrderView(View):

    def get(self, request):
        if request.user.is_authenticated():
            if request.session.get('cart', False):
                u = MyUsers.objects.get(user_id=request.user.id)
                order = Orders.objects.create(
                    user_id=u.id,
                    total_sum=request.session.get('total_cart', False)
                )
                list_product = request.session.get('cart', False)
                for product in list_product:
                    OrderProducts.objects.create(
                        quantity=product.quantity_in_cart,
                        sum=product.price,
                        order_id=order.id,
                        product_id=product.id
                    )
                    prod = Products.objects.get(id=product.id)
                    new_quantity = prod.quantity - product.quantity_in_cart
                    Products.objects.filter(id=product.id).update(quantity=new_quantity)
                request.session.pop('cart')
        return HttpResponseRedirect('/accounts/profile/')
