from django.shortcuts import render
from requests import Response
from rest_framework import viewsets, renderers
from .serializers import ProductsSerializer
from shop.models import Products
from rest_framework.decorators import detail_route

# Create your views here.


class ProductsViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
