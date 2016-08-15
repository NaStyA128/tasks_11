from django.db import models
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

# Create your models here.
# Users = get_user_model()


class MyUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13, verbose_name=_("Phone"))

    @python_2_unicode_compatible
    def __str__(self):
        return self.user.username


class Categories(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    @python_2_unicode_compatible
    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        verbose_name=_("Category")
    )
    image = models.ImageField(
        upload_to='photos/',
        max_length=255,
        verbose_name=_("Image")
    )
    size = models.CharField(max_length=10, verbose_name=_("Size"))
    colour = models.CharField(max_length=40, verbose_name=_("Colour"))
    price = models.FloatField(verbose_name=_("Price"))
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))

    @python_2_unicode_compatible
    def __str__(self):
        return '%s, %s, %s' % \
               (self.name, self.size, self.colour)


class Orders(models.Model):
    user = models.ForeignKey(
        # settings.AUTH_USER_MODEL,
        MyUsers,
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )
    products = models.ManyToManyField(
        Products,
        through='OrderProducts',
        verbose_name=_("Products")
    )
    total_sum = models.FloatField(verbose_name=_("Total sum"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))


class OrderProducts(models.Model):
    order = models.ForeignKey(
        Orders,
        on_delete=models.CASCADE,
        verbose_name=_("Order")
    )
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        verbose_name=_("Product")
    )
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))
    sum = models.FloatField(verbose_name=_("Sum"))


# class Buyers(models.Model):
#     name = models.CharField(max_length=100, verbose_name=_("Name"))
#     phone = models.CharField(max_length=13, verbose_name=_("Phone"))


class Tree(models.Model):
    node = models.ForeignKey('self')
