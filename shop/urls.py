from django.conf.urls import url, include
from django.contrib import admin

from .views import (
    products,
    products_id,
)

urlpatterns = [
    url(r'^$', products),
    url(r'^(?P<id>\d+)/$', products_id),
]