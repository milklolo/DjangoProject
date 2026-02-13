from django.db import models
import uuid

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text='uuid')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name

class Sales(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text='uuid')
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text='uuid')
    order_date = models.DateField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )

    sales = models.ForeignKey(
        Sales, on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    def __str__(self):
        return f"Order {self.id}"
