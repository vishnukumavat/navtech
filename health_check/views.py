from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import django
from django.conf import settings
from health_check.serializers import TestSerializer

class TestAPIView(APIView):
    def getDBConnectionStatus(self):
        dbConnectionErrors = django.db.connection.ensure_connection()
        dbConnection = False
        if not dbConnectionErrors:
            dbConnection = True
        return dbConnection

    def get(self, request, *args, **kwargs):
        return Response({
            "result": "Success", 
            "data_base_connection":self.getDBConnectionStatus(), 
            "message":"Hello from GET request"
        }, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            response_data = {
                "result": "Success", 
                "data_base_connection":self.getDBConnectionStatus(), 
                "message":"Hello from POST request"
            }
            result = serializer.complete_task_and_get_data()
            response_data.update(result)
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)