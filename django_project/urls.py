"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from shop.views import (
    UserProfile,
    RegistrationUser,
    LoginUser,
    LogoutView,
    CartView,
    MakeOrderView,
    CreateOrderView,
)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^cart/create_order/', CreateOrderView.as_view(), name='create_order'),
    url(r'^cart/order/', MakeOrderView.as_view(), name='make_order'),
    url(r'^cart/', CartView.as_view(), name='cart'),
    url(r'^accounts/login/', LoginUser.as_view()),
    url(r'^accounts/logout/', LogoutView.as_view()),
    url(r'^accounts/profile/', UserProfile.as_view()),
    url(r'^accounts/', RegistrationUser.as_view()),
    url(r'^', include("shop.urls")),
]

if settings.DEBUG:
    urlpatterns.extend(
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    )
    urlpatterns.extend(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
