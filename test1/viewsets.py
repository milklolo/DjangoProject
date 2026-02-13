from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Product, Sales, Order
from .serializers import ProductSerializer, SalesSerializer, OrderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SalesViewSet(viewsets.ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
