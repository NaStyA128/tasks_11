from django.conf.urls import url, include
from django.contrib import admin

from .views import (
    CategoriesList,
    ProductsList,
    ProductDetail,
    AddProduct,
)

urlpatterns = [
    url(r'^$', CategoriesList.as_view()),
    url(r'^(\d+)/$', ProductsList.as_view()),
    url(r'^(\d+)/(?P<pk>\d+)/$', ProductDetail.as_view()),
    url(r'^add_product/$', AddProduct.as_view()),
]