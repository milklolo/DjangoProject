from django.shortcuts import render

from test1.models import Product,Sales,Order


def product_frontend(request):
    products = Product.objects.all()
    return render(request, "test1/products.html",{"products": products})

def sales_frontend(request):
    sales = Sales.objects.all()
    return render(request, "test1/sales.html")

def order_frontend1(request):
    # orders = Order.objects.all()
    # products = Product.objects.all()
    # sales = Sales.objects.all()
    # return render(request, "test1/orders.html",
    #               {"orders": orders,
    #                "products": products,
    #                "sales": sales})
    return render(request, "test1/orders1.html")

def order_frontend(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    sales = Sales.objects.all()
    return render(request, "test1/orders.html",
                  {"orders": orders,
                   "products": products,
                   "sales": sales})
