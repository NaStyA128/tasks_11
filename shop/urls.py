from django.conf.urls import url, include
from django.contrib import admin

from .views import (
    IndexList,
    ProductsList,
    ProductDetail,
    AddProduct,
    UpdateProduct,
    DeleteProduct,
)

urlpatterns = [
    url(r'^$', IndexList.as_view()),
    url(r'^(\d+)/$', ProductsList.as_view(), name='products-list'),
    url(r'^(\d+)/(?P<pk>\d+)/$', ProductDetail.as_view()),
    url(r'^edit_product/(?P<pk>\d+)/$', UpdateProduct.as_view()),
    url(r'^add_product/$', AddProduct.as_view()),
    url(r'^delete_product/(?P<pk>\d+)/$', DeleteProduct.as_view()),
]