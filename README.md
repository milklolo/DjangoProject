DRF test
poetry 建django

#產品 (產品id, 產品名稱, 產品售價)  
#業務人員 (業務id, 業務名)  
#訂單 (訂單編號, 訂單日期, 產品id, 數量, 業務id)  
#產品管理介面  
#業務人員管理介面  
#訂單管理介面  

#新專案 django poetry  
pyproject.toml 

requires-python = "^3.11"  
[tool.poetry]  
package-mode = false  
降板  
poetry add "django>=4.2,<5.0"  

poetry run django-admin startproject <projectname> .  
後面的點要打  
poetry run python manage.py startapp<name>  
settings.py add <name>  
poetry run python manage.py migrate  
設定到這差不多就好了  
model.py建資料庫  
Foreignkey  
在Order裡面打這個的話就是Order要刪的時候會間去確認sales有沒有跟你要刪的這筆資料有關聯  
sales = models.ForeignKey(Sales, on_delete=models.CASCADE)  
ID那幾行要打  

#產資料表  
python manage.py makemigrations  
python manage.py migrate  
#如果要資料庫的話先刪db跟migrations>0001  
再重跑  
python manage.py makemigrations  
python manage.py migrate  

amdin要加  
from .models import Product, Sales, Order  

admin.site.register(Product)  
admin.site.register(Sales)  
admin.site.register(Order)  

#註冊帳號(cmd  
python manage.py createsuperuser  
python manage.py runserver  

serializers  
view  
url  
#app下要建一個urls.py  
專案(myproject)的則要加入app的路徑  
path('', include('test1.urls')),  

#run  
python manage.py runserver  
就可以進到資料表的網頁 /admin  

#建網頁，先建templates在裡面放一個base.html  
	<!DOCTYPE html>  
	<html lang="en">  
	<head>{% block title %}My App{% endblock %}</head>  
	<body>  
	{% block content %}  
	{% endblock %}  
	</body>  
	{% block scripts %}{% endblock %}  

再建個資料夾(test1)放子html(test1/templates/test1/product.html)  
	{% extends 'base.html' %}  
	{% block title %}Product List{% endblock %}  
	{% block content %}  
	{% endblock %}   
	{% block scripts %}  
	{% endblock %}  

views的return要加"test1/products.html",{"products": products}  
資料才可以在前端用  
	<tbody>  
        {% for product in products %}<!--  views裡面的回傳值      -->  
        <tr>  
            <td>{{ product.id }}</td>  
            <td>{{ product.name }}</td>  
            <td>{{ product.price }}</td>  
        </tr>  
        {% endfor %}  
    </tbody>  

#以上是環境及基礎網頁

#如果要在一個頁面抓多個資料表的話views.py要加要的資料表

=======
一筆訂單多項商品
serializer
加入OrderItemSerializer讓多筆的東西有地方放
order加入update create

viewset
OrderViewSet加入update create


