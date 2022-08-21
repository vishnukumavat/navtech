from itertools import product
from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.utils import timezone
import datetime

class Products(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField(null=True, blank=True)
    available_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name
    
    class Meta:
        db_table = 'products'

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'orders'


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'price', 'available_quantity')


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'user', 'product', 'quantity', 'price')
    list_filter = (
        ('created_at', DateFieldListFilter),
    )