from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
import io, csv, pandas as pd
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from orders.serializers import PlaceOrderSerializer, CreateUpdateProductSerializer
from orders.services.orders_statisctics import GetOrderStatistics


class CreateUpdateProductAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = CreateUpdateProductSerializer(data=request.data)
        if serializer.is_valid():
            message, is_valid = serializer.valid_file()
            if is_valid:
                result = serializer.complete_task_and_get_data()
                return Response(result, status=status.HTTP_200_OK)
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GetOrderStatsticsAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        return Response(GetOrderStatistics().get_data(), status=status.HTTP_200_OK)


class PlaceOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data.update({"user_id": request.user.id})
        serializer = PlaceOrderSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.complete_task_and_get_data()
            return Response(result, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
