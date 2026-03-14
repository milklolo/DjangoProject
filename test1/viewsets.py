from django.shortcuts import render
from rest_framework import viewsets, status
from .models import product, sales, order
from .serializers import ProductSerializer, SalesSerializer, OrderSerializer
from rest_framework.response import Response
from django.db import transaction

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = product.objects.all()
    serializer_class = ProductSerializer


class SalesViewSet(viewsets.ModelViewSet):
    queryset = sales.objects.all()
    serializer_class = SalesSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        # 1. 取得前端 serialize() 送過來的多個陣列
        products = request.data.getlist('product[]')
        quantities = request.data.getlist('quantity[]')

        # 2. 手動組成 Serializer 想要的 items 格式
        items_data = []
        for p_id, qty in zip(products, quantities):
            if p_id:  # 確保有選商品才加入
                items_data.append({
                    'product': p_id,
                    'quantity': qty
                })

        # 3. 把組好的資料塞回給 Serializer 驗證
        # 我們複製一份 request.data 並修改它
        data = request.data.copy()
        data.setlist('items', items_data)  # 這裡必須是 JSON 格式，但傳統 POST 很難處理巢狀

        # --- 如果上面的 setlist 還是報錯，改用下面這個萬用方案 ---
        mutable_data = {
            'order_date': request.data.get('order_date'),
            'sales': request.data.get('sales'),
            'items': items_data  # 這是關鍵：把 product[] 轉成 items 結構
        }

        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 1. 取得前端送過來的多個陣列
        products = request.data.getlist('product[]')
        quantities = request.data.getlist('quantity[]')

        # 2. 手動組成 Serializer 想要的 items 結構
        items_data = []
        for p_id, qty in zip(products, quantities):
            if p_id:
                items_data.append({
                    'product': p_id,
                    'quantity': qty
                })

        # 3. 重新構建要交給 Serializer 驗證的資料
        # 注意：這裡的 Key 要對應你 Serializer 的欄位名稱
        mutable_data = {
            'order_date': request.data.get('order_date'),
            'sales': request.data.get('sales'),
            'items': items_data
        }

        # 4. 執行標準的 DRF 驗證與存檔流程
        serializer = self.get_serializer(instance, data=mutable_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
