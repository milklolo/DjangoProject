from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = '__all__'
        extra_kwargs = {
            'image1': {'required': False, 'allow_null': True}
        }

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
    product_image = serializers.SerializerMethodField()
    class Meta:
        model = orderItem
        fields = '__all__'
        read_only_fields = ('order',) #這樣驗證時就不會要求提供 order ID，資料就能順利進入 validated_data

    def get_product_image(self, obj):
        # 關鍵防呆：先檢查 product 是否有 image1，再檢查 image1 是否有檔案
        try:
            if obj.product and obj.product.image1 and hasattr(obj.product.image1, 'url'):
                return obj.product.image1.url
        except ValueError:
            # 如果資料庫有欄位但檔案不存在，會跳到這裡
            return None
        return None


class OrderSerializer(serializers.ModelSerializer):
    # 確保這裡的 items 允許寫入 (不要加 read_only=True)
    items = OrderItemSerializer(many=True)
    sales_name = serializers.CharField(source='sales.name', read_only=True)

    class Meta:
        model = order
        fields = '__all__'

    def get_product_image(self, obj):
        # 取得商品關聯的圖片路徑
        if obj.product.image1:
            return obj.product.image1.url
        return None

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