from rest_framework import serializers
from shop.models import Products


class ProductsSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Products
        fields = '__all__'
