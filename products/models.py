from django.db import models
from categories.models import Category
from brands.models import Brand


class Product(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')

    def __str__(self):
        return self.title
