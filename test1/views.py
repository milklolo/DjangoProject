from django.shortcuts import render

from test1.models import product,sales,order


def product_frontend(request):
    products = product.objects.all()
    return render(request, "test1/products.html",{"products": products})

def product_frontend_n(request):
    return render(request, "test1/products_n.html")

def sales_frontend(request):
    return render(request, "test1/sales.html")

def sales_frontend_n(request):
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
    orders = order.objects.all()
    products = product.objects.all()
    saleso = sales.objects.all()
    return render(request, "test1/orders.html",
                  {"orders": orders,
                   "products": products,
                   "sales": saleso})

def order_frontend_n(request):
    orders = order.objects.all()
    products = product.objects.all()
    saleso = sales.objects.all()
    return render(request, "test1/orders_n.html",
                  {"orders": orders,
                   "products": products,
                   "sales": saleso})