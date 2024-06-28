from api.services.EquipmentService import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

equipmentService = EquipmentService()

class EquipmentListView(APIView):
    permission_classes = [AllowAny,]
    def get(self, request, format=None):
        """
        Return list of equipmemnts.
        """
        result = equipmentService.EquipmentList(request)
        return Response(result, status = status.HTTP_200_OK)

class SelectedEquipmentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        result = equipmentService.SelectedEquipments(request)
        return Response(result, status=status.HTTP_201_CREATED)


