from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import ProductViewSet, SalesViewSet, OrderViewSet
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'products', ProductViewSet,basename='products')
router.register(r'sales', SalesViewSet,basename='sales')
router.register(r'orders', OrderViewSet,basename='orders')

urlpatterns = [
    path('', include(router.urls)),
    path('products-page/',views.product_frontend, name='products-page'),
    path('products-page-new/',views.product_frontend_n ,name='products-page-n'),
    path('sales-page/',views.sales_frontend ,name='sales-page'),
    path('sales-page-new/',views.sales_frontend_n ,name='sales-page-n'),
    path('order-page/',views.order_frontend ,name='orders-page'),
    path('order-page1/',views.order_frontend1 ,name='orders-page1'),
    path('order-page-new/',views.order_frontend_n ,name='orders-page-n'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
