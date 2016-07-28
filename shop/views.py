from django.shortcuts import render, HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404

# Create your views here.
from .models import (
    Categories,
    Products,
)
from .forms import CategoryForm

"""
# @require_http_method(['GET', 'POST'])
# @require_GET()
def index(request):
    # можно упростить, использ. декоратор
    # if request.method == 'POST':
    try:
        id = Categories.objects.get(id=id)
    except:
        raise Http404
    return render(request, 'index.html', {'id': id})
"""


def products(request):
    if request.method == 'GET':
        form = CategoryForm()
    elif request.method == 'POST':
        form = CategoryForm(request.POST)
    # if form.is_valid():
    #     form.save()
    prod = Products.objects.all()
    context = {
        'products': prod,
        'form': form,
    }
    return render(request, 'products.html', context)


def products_id(request, id):
    # try:
    # get_list_or_404
    prod = get_object_or_404(Products, id=id)
    context = {
        'product': prod,
    }
    # except:
    #     raise Http404
    return render(request, 'product.html', context)
