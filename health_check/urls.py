from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from health_check.views import TestAPIView

urlpatterns = [
    path(r'test/', TestAPIView.as_view(), name='TestAPI'),
]

urlpatterns = format_suffix_patterns(urlpatterns, suffix_required=False)