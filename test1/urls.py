from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import ProductViewSet, SalesViewSet, OrderViewSet
from . import views

router = DefaultRouter()
router.register(r'products', ProductViewSet,basename='products')
router.register(r'sales', SalesViewSet,basename='sales')
router.register(r'orders', OrderViewSet,basename='orders')

urlpatterns = [
    path('', include(router.urls)),
    path('products-page/',views.product_frontend, name='products-page'),
    path('sales-page/',views.sales_frontend ,name='sales-page'),
    path('order-page/',views.order_frontend ,name='orders-page'),
    path('order-page1/',views.order_frontend1 ,name='orders-page1'),
]
