from django.db import models
import uuid

class product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text='uuid')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name

class sales(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text='uuid')
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

# class order(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text='uuid')
#     order_date = models.DateField()
#     product = models.ForeignKey(
#         product, on_delete=models.PROTECT
#     )
#
#     sales = models.ForeignKey(
#         sales, on_delete=models.PROTECT
#     )
#     quantity = models.IntegerField()
#     def __str__(self):
#         return f"Order {self.id}"
class order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_date = models.DateField()
    sales = models.ForeignKey(sales, on_delete=models.PROTECT)
    # 移除原本的 product 和 quantity

class orderItem(models.Model):
    order = models.ForeignKey(order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)