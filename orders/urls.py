from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from orders.views import PlaceOrderAPIView,CreateUpdateProductAPIView,GetOrderStatsticsAPIView

urlpatterns = [
    path(r'create_update_product/', CreateUpdateProductAPIView.as_view(), name='CreateUpdateProduct'),
    path(r'order_stats/', GetOrderStatsticsAPIView.as_view(), name='GetOrderStatstics'),
    path(r'place_order/', PlaceOrderAPIView.as_view(), name='PlaceOrder'),
]

urlpatterns = format_suffix_patterns(urlpatterns, suffix_required=False)