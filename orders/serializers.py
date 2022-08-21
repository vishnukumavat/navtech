import re
from rest_framework import serializers
from orders.models import Products
from django.conf import settings
from orders.services.utils import readInMemoryUploadedCSVFile
from orders.services.create_update_products import CreateOrUpdateProducts
from orders.services.place_order import PlaceOrder


class CreateUpdateProductSerializer(serializers.Serializer):
    file = serializers.FileField()

    productList = [] 

    def valid_file(self):
        uploaded_csv_file = self.validated_data['file']
        filename = uploaded_csv_file.name
        if filename.endswith(settings.PRODUCT_FILE_UPLOAD_TYPE):
            if uploaded_csv_file.size < int(settings.MAX_UPLOAD_SIZE):
                dataList = readInMemoryUploadedCSVFile(uploaded_csv_file)
                if dataList:
                    receivedFields = dataList[0].keys()
                    missingFields = set(settings.PRODUCT_FILE_FIELDS).difference(receivedFields)
                    if not missingFields:
                        self.productList = dataList
                        return "", True
                    return f"{', '.join(missingFields)} - missing in csv file", False
                return "Empty CSV file", False
            return f"File size must not exceed {settings.MAX_UPLOAD_SIZE} bytes ", False
        return "Please upload .csv extension files only", False
    
    def complete_task_and_get_data(self):
        return CreateOrUpdateProducts(self.productList).perform_task()


class OrdersSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=200)
    quantity = serializers.IntegerField()

class PlaceOrderSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    orders = serializers.ListField(child=OrdersSerializer(), required=True, allow_empty=False)

    def complete_task_and_get_data(self):
        return PlaceOrder(**self.validated_data).perform_task()