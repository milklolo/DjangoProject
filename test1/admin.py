from django.contrib import admin
from .models import Product, Sales, Order
# Register your models here.
admin.site.register(Product)
admin.site.register(Sales)
admin.site.register(Order)