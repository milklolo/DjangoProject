from django.shortcuts import render
from rest_framework import viewsets, status
from .models import product, sales, order, orderItem
from .serializers import ProductSerializer, SalesSerializer, OrderSerializer
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Q
from model_utils import Choices
from django.conf import settings
import os


# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = product.objects.all()
    serializer_class = ProductSerializer

    # CRUD要加此段
    def list(self, request, **kwargs) -> dict or None:
        try:
            dParameter = self.__query_by_args(**request.query_params)
            serializer = ProductSerializer(dParameter["items"], many=True)
            result = dict()
            result["data"] = serializer.data
            result["draw"] = dParameter["draw"]
            result["recordsTotal"] = dParameter["total"]
            result["recordsFiltered"] = dParameter["count"]
            return Response(
                result, status=status.HTTP_200_OK, template_name=None, content_type=None
            )

        except Exception as e:
            return Response(
                e,
                status=status.HTTP_404_NOT_FOUND,
                template_name=None,
                content_type=None,
            )

    def __query_by_args(self, **kwargs) -> dict:
        ORDER_COLUMN_CHOICES = Choices(
            ("0", "id"),
            ("1", "name"),
            ("2", "price"),
            ("3", "image1"),
        )

        draw: int = int(kwargs.get("draw", None)[0])
        length: int = int(kwargs.get("length", None)[0])
        start: int = int(kwargs.get("start", None)[0])
        search_value: str = kwargs.get("search[value]", None)[0]
        order_column: str = kwargs.get("order[0][column]", None)[0]
        order: str = kwargs.get("order[0][dir]", None)[0]

        order_column = ORDER_COLUMN_CHOICES[order_column]
        # django orm '-' -> desc
        if order == "desc":
            order_column = "-" + order_column

        # Mutiple column order
        order_column_1 = ''
        if (kwargs.get('order[1][column]', None)) is not None:
            order_column_1 = kwargs.get('order[1][column]', None)[0]
            order_column_1 = ORDER_COLUMN_CHOICES[order_column_1]
            order_1 = kwargs.get('order[1][dir]', None)[0]
            if order_1 == 'desc':
                order_column_1 = '-' + order_column_1

        queryset = product.objects.all()
        total = queryset.count()

        if search_value:
            queryset = queryset.filter(
                Q(name__icontains=search_value)
                | Q(id__icontains=search_value)
                | Q(price__icontains=search_value)
                | Q(image1__icontains=search_value)
            )

        count = queryset.count()
        if (kwargs.get('order[1][column]', None)) is None:
            queryset = queryset.order_by(order_column)[start:start + length]
        else:
            queryset = queryset.order_by(order_column, order_column_1)[start:start + length]
        return {"items": queryset, "count": count, "total": total, "draw": draw}

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data

        # 取得「更新前」的舊圖片物件
        old_image = instance.image1

        # 1. 處理點擊 X 刪除圖片
        if data.get('clear_image') == 'true':
            if old_image:
                old_image.delete(save=False)  # 這會刪除硬碟檔案並清空欄位
            instance.image1 = None
            instance.save()

        # 2. 處理上傳新圖片（自動覆蓋並刪除舊的）
        if 'image1' in request.FILES:
            # 如果有舊圖且新圖進來了，先刪除舊的實體檔案
            if old_image:
                old_image.delete(save=False)

            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(image1=request.FILES['image1'])
        else:
            # 沒傳新圖，也沒點刪除，就只更新文字資料
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data)

    def perform_destroy(self, instance):
        # 1. 先獲取圖片路徑
        image_path = instance.image1.path if instance.image1 else None

        # 2. 執行刪除資料庫紀錄
        instance.delete()

        # 3. 刪除資料庫成功後，再刪除實體檔案
        if image_path and os.path.isfile(image_path):
            os.remove(image_path)


class SalesViewSet(viewsets.ModelViewSet):
    queryset = sales.objects.all()
    serializer_class = SalesSerializer

    # CRUD要加此段
    def list(self, request, **kwargs) -> dict or None:
        try:
            dParameter = self.__query_by_args(**request.query_params)
            serializer = SalesSerializer(dParameter["items"], many=True)
            result = dict()
            result["data"] = serializer.data
            result["draw"] = dParameter["draw"]
            result["recordsTotal"] = dParameter["total"]
            result["recordsFiltered"] = dParameter["count"]
            return Response(
                result, status=status.HTTP_200_OK, template_name=None, content_type=None
            )

        except Exception as e:
            return Response(
                e,
                status=status.HTTP_404_NOT_FOUND,
                template_name=None,
                content_type=None,
            )

    def __query_by_args(self, **kwargs) -> dict:
        ORDER_COLUMN_CHOICES = Choices(
            ("0", "id"),
            ("1", "name"),
            ("2", "price"),
            ("3", "image1"),
        )

        draw: int = int(kwargs.get("draw", None)[0])
        length: int = int(kwargs.get("length", None)[0])
        start: int = int(kwargs.get("start", None)[0])
        search_value: str = kwargs.get("search[value]", None)[0]
        order_column: str = kwargs.get("order[0][column]", None)[0]
        order: str = kwargs.get("order[0][dir]", None)[0]

        order_column = ORDER_COLUMN_CHOICES[order_column]
        # django orm '-' -> desc
        if order == "desc":
            order_column = "-" + order_column

        # Mutiple column order
        order_column_1 = ''
        if (kwargs.get('order[1][column]', None)) is not None:
            order_column_1 = kwargs.get('order[1][column]', None)[0]
            order_column_1 = ORDER_COLUMN_CHOICES[order_column_1]
            order_1 = kwargs.get('order[1][dir]', None)[0]
            if order_1 == 'desc':
                order_column_1 = '-' + order_column_1

        queryset = sales.objects.all()
        total = queryset.count()

        if search_value:
            queryset = queryset.filter(
                Q(name__icontains=search_value)
                | Q(id__icontains=search_value)
            )

        count = queryset.count()
        if (kwargs.get('order[1][column]', None)) is None:
            queryset = queryset.order_by(order_column)[start:start + length]
        else:
            queryset = queryset.order_by(order_column, order_column_1)[start:start + length]
        return {"items": queryset, "count": count, "total": total, "draw": draw}


class OrderViewSet(viewsets.ModelViewSet):
    queryset = order.objects.all()
    serializer_class = OrderSerializer

    # 1. 加入 list 方法，對接 DataTables
    def list(self, request, **kwargs):
        try:
            # 傳入 request.query_params (QueryDict)
            dParameter = self.__query_by_args(request.query_params)
            serializer = OrderSerializer(dParameter["items"], many=True)
            result = {
                "draw": dParameter["draw"],
                "recordsTotal": dParameter["total"],
                "recordsFiltered": dParameter["count"],
                "data": serializer.data,
            }
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            # 這裡建議印出詳細錯誤到終端機，方便 debug
            print(f"Server-side Error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def __query_by_args(self, query_params) -> dict:
        # 1. 定義排序欄位對應
        ORDER_COLUMN_CHOICES = {
            "0": "id",
            "1": "order_date",
            "3": "sales_name",  # 根據你 models 的 sales 關聯欄位名稱調整
        }

        # 2. 安全獲取參數 (使用 .get 而非 [0]，避免 QueryDict list 報錯)
        draw = int(query_params.get("draw", 1))
        length = int(query_params.get("length", 10))
        start = int(query_params.get("start", 0))
        search_value = query_params.get("search[value]", "")
        order_column_index = query_params.get("order[0][column]", "0")
        order_dir = query_params.get("order[0][dir]", "asc")

        # 3. 處理排序
        order_column = ORDER_COLUMN_CHOICES.get(order_column_index, "id")
        if order_dir == "desc":
            order_column = "-" + order_column

        # 4. 基礎 QuerySet (建議加上 select_related 優化效能)
        queryset = order.objects.select_related('sales').all()
        total = queryset.count()

        # 5. 搜尋過濾
        # 外表的話 model__變數__icontains
        if search_value:
            queryset = queryset.filter(
                Q(id__icontains=search_value) |
                Q(order_date__icontains=search_value) |
                Q(order_sales__icontains=search_value) |
                Q(sales__name__icontains=search_value) |
                Q(items__product__name__icontains=search_value)
            )

        count = queryset.count()

        # 6. 分頁
        queryset = queryset.order_by(order_column)[start: start + length]

        return {"items": queryset, "count": count, "total": total, "draw": draw}

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