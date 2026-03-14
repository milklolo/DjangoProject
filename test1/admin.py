from django.contrib import admin
from .models import product, sales, order
# Register your models here.
admin.site.register(product)
admin.site.register(sales)
admin.site.register(order)