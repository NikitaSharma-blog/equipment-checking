from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.services.UserService import *

userService = UserService()


class LoginView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request, format=None):
        result = userService.login(request)
        return Response(result, status=status.HTTP_200_OK)


class UserStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, format=None):
        result = userService.SaveEmployeeStatus(request)
        return Response(result, status=status.HTTP_201_CREATED)