from django.shortcuts import render
from rest_framework import viewsets, status
from .models import product, sales, order
from .serializers import ProductSerializer, SalesSerializer, OrderSerializer

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = product.objects.all()
    serializer_class = ProductSerializer


class SalesViewSet(viewsets.ModelViewSet):
    queryset = sales.objects.all()
    serializer_class = SalesSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = order.objects.all()
    serializer_class = OrderSerializer
