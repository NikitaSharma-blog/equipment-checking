from re import T
from .UserBaseService import UserBaseService
from api.models import *
from api.serializers import UserLoginDetailSerializer, UserStatusSerializer,SelectedEquipmentSerializer, DeviceTokenSerializer
from rest_framework import status
import jwt
from rest_framework_jwt.settings import api_settings
from betul_electronics import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token

from fcm_django.models import FCMDevice

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserService():

    def login(self, request):
        print("login")
        validated_data = self.validate_auth_data (request)
        print("login")
        email = request.data['email']
        email = email.lower ()
        password = request.data['password']
        device_token =  request.data.get('device_token', None)
        try:
            login_user = authenticate(email=email, password=password)
        except:
            login_user = None
        if login_user is not None:
            login(request, login_user)
            serializer = UserLoginDetailSerializer (login_user)
            user_id = serializer.data.get("id")
            instance = User.objects.get(id=user_id)
            instance.device_token = device_token
            instance.save()
            serializer = serializer.data
            token, created = Token.objects.get_or_create(user=login_user)
            print(token.key)
            serializer['token'] = token.key 
            print()
            self.addFcm(request, login_user)

            return ({"data": serializer, "code": status.HTTP_200_OK, "message": "LOGIN_SUCCESSFULLY"})

        return ({"message": None, "code": status.HTTP_401_UNAUTHORIZED, "message": "Your email or password is incorrect!"})


    def validate_auth_data(self, request):
        error = {}
        if not request.data.get ('email'):
            error.update ({'email': "FIELD_REQUIRED"})

        if not request.data.get ('password'):
            error.update ({'password': "FIELD_REQUIRED"})

        if request.headers.get ('device-type') == 'android' or request.headers.get ('device-type') == 'ios':
            if not request.data.get ('device_id'):
                error.update ({'device_id': "FIELD_REQUIRED"})
        if error:
            raise ValidationError (error)
   
    def SaveEmployeeStatus(self, request):
        id = request.user.id
        print(id)
        user_status = request.data.get('user_status', None)
        serialize_data = {"user_status":user_status}
        instance = User.objects.get(id=id)
        print("status", instance.user_status)
        serializer = UserStatusSerializer(instance=instance, data=serialize_data, partial=True)
        message = "You did not confirm you wear personal equipment, but you are climbing up already"
        # serializer = SelectedEquipmentSerializer(data=serialize_data, partial=True)
        equip_user = SelectedEquipments.objects.filter(user_id=id).last()
        print("Equip user in service", equip_user)
        equip = SelectedEquipments.selected_equipment.through.objects.filter(selectedequipments_id=equip_user).values_list('equipments_id', flat=True)
        print("equip ids", len(equip))
        all_equipmets = Equipments.objects.all().exclude(id__in=equip)
        
        if serializer.is_valid():
            print(instance.user_status)
            # if len(equip)<17 and (user_status==2 and instance.user_status!=2):
            #     print("###########in if###########")
            #     self.send_loggin_push_notification(instance, message)
            #     self.send_loggin_push_notification(instance.employee_supervisor, message)
            if len(equip)<17 and user_status==2:
                print("###########in elif###########")
                self.send_loggin_push_notification(instance, message)
                self.send_loggin_push_notification(instance.employee_supervisor, message)

            serializer.save()
            result = {'data': serializer.data, 'code': status.HTTP_200_OK, 'message': "User Updated Succesfully"}
        else:
            result = {'data': serializer.errors, 'code': status.HTTP_400_BAD_REQUEST, 'message': "Data is not valid"}
        return result


    def addFcm(self, request, user):
        """
        Use this endpoint to insert fc requirements

        """
        # try:
        print(user)
        """
         here registration_id is the device_token and device_is is the id of device
        """
        DeviceAccounts = FCMDevice.objects.filter(registration_id = request.data["registration_id"])
        if len(DeviceAccounts)>0:
            for oneAccount in DeviceAccounts:
                oneAccount.delete()

        DeviceAccounts = FCMDevice.objects.filter(user = user)
        if len(DeviceAccounts)>0:
            for oneAccount in DeviceAccounts:
                oneAccount.delete()
        # return Response({"success": True}, status=status.HTTP_200_OK)
        
        instance, created = FCMDevice.objects.get_or_create(user=user)
        instance.type = request.data["device_type"]
        instance.registration_id = request.data["registration_id"]
        instance.device_id = request.data["device_id"]
        instance.is_active = True
        instance.save()

        return "success"

    def send_loggin_push_notification(self, user, message=None):
        from api.utils import send_push_notification

        # message = "Logged in Succesfully."
    
        send_push_notification(False, None, user, message, None)
        
        
                
