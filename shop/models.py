from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
# Users = get_user_model()


class Categories(models.Model):
    name = models.CharField(max_length=50)

    @python_2_unicode_compatible
    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        upload_to='photos/',
        max_length=255,
    )
    size = models.CharField(max_length=10)
    colour = models.CharField(max_length=40)
    price = models.FloatField()
    quantity = models.PositiveIntegerField()

    @python_2_unicode_compatible
    def __str__(self):
        return '%s, %s, %s' % \
               (self.name, self.size, self.colour)


class Orders(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    products = models.ManyToManyField(Products, through='OrderProducts')
    total_sum = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class OrderProducts(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sum = models.FloatField()


class Tree(models.Model):
    node = models.ForeignKey('self')
