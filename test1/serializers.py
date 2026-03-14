from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = '__all__'

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = sales
        fields = '__all__'


# class OrderSerializer(serializers.ModelSerializer):
#     product_id = serializers.CharField(source='product.id', read_only=True)
#     product_name = serializers.CharField(source='product.name', read_only=True)
#     product_price = serializers.CharField(source='product.price', read_only=True)
#     sales_id = serializers.CharField(source='sales.id', read_only=True)
#     sales_name = serializers.CharField(source='sales.name', read_only=True)
#     # product = ProductSerializer(read_only=True)
#     # sales = SalesSerializer(read_only=True)
#
#     class Meta:
#         model = order
#         fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = orderItem
        fields = ['product', 'product_name', 'product_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    # 確保這裡的 items 允許寫入 (不要加 read_only=True)
    items = OrderItemSerializer(many=True)
    sales_name = serializers.CharField(source='sales.name', read_only=True)

    class Meta:
        model = order
        fields = ['id', 'order_date', 'sales', 'sales_name', 'items']

    def create(self, validated_data):
        # 處理新增邏輯
        items_data = validated_data.pop('items')
        new_order = order.objects.create(**validated_data)
        for item_data in items_data:
            orderItem.objects.create(order=new_order, **item_data)
        return new_order

    def update(self, instance, validated_data):
        # 處理修改邏輯 (解決你遇到的 AssertionError)
        items_data = validated_data.pop('items', None)

        # 1. 更新主表 (Order) 的欄位
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.sales = validated_data.get('sales', instance.sales)
        instance.save()

        # 2. 更新明細表 (OrderItem)
        if items_data is not None:
            # 最簡單暴力的作法：刪除該訂單原有的所有明細，重新建立
            # 注意：instance.items 的 'items' 必須是你 Model 外鍵設定的 related_name
            instance.items.all().delete()

            for item_data in items_data:
                orderItem.objects.create(order=instance, **item_data)

        return instance