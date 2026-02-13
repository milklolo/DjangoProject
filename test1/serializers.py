from rest_framework import serializers
from .models import Product, Sales, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    sales_name = serializers.CharField(source='sales.name', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
