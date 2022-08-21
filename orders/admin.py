from django.contrib import admin
from orders.models import Products,Orders,ProductsAdmin,OrdersAdmin

# Register your models here.
admin.site.register(Products,ProductsAdmin)
admin.site.register(Orders,OrdersAdmin)