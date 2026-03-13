from django.shortcuts import render

from test1.models import Product,Sales,Order


def product_frontend(request):
    products = Product.objects.all()
    return render(request, "test1/products.html",{"products": products})

def product_frontend_n(request):
    products = Product.objects.all()
    return render(request, "test1/products_n.html",{"products": products})

def sales_frontend(request):
    sales = Sales.objects.all()
    return render(request, "test1/sales.html")

def sales_frontend_n(request):
    sales = Sales.objects.all()
    return render(request, "test1/sales_n.html")

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

def order_frontend_n(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    sales = Sales.objects.all()
    return render(request, "test1/orders_n.html",
                  {"orders": orders,
                   "products": products,
                   "sales": sales})