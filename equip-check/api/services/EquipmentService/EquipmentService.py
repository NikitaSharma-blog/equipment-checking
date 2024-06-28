import imp
from api.models import *
from api.serializers import *
# from rest_framework.status import *
from django.utils import timezone
from datetime import datetime

from rest_framework import status
from fcm_django.models import FCMDevice
from api.utils import (send_push_notification)
from api.services.UserService.UserService import UserService

class EquipmentService():

    def EquipmentList(self, request):
        equipmment_list = Equipments.objects.all()
        serializer = EquipmentListSerializer(equipmment_list, many=True)
        result = serializer.data
        return {"data":result, 'code': status.HTTP_200_OK, 'message': "OK"}


    def SelectedEquipments(self, request):
        # user_id = request.data.get("user_id", None)
        equipments = request.data.get("equipment_id", None)
        user_id = request.user.id
        print("user id", user_id)
        user_obj = User.objects.get(id=user_id)
        # user_id = user_id, user_obj.employee_supervisor.id
        user_obj_status = user_obj.user_status
        serialize_data = {'user_id':user_id}
        serializer = SelectedEquipmentSerializer(data=serialize_data, partial=True)
        equip_user = SelectedEquipments.objects.filter(user_id=user_id)
        print("Equip user", equip_user)
        equip = SelectedEquipments.selected_equipment.through.objects.filter(selectedequipments_id__in=equip_user)
        all_equipmets = Equipments.objects.all().exclude(id__in=equip)
        length_dict = {key: len(value) for key, value in request.data.items()}
        print("len dict", length_dict)
        length_key = length_dict['equipment_id']
        # print("range", request.data['equipment_id'].count())
        if serializer.is_valid():
            serializer.save()
            selected_id = SelectedEquipments.objects.get(id=serializer.data.get("id"))
            selected_id.selected_equipment.set(equipments)
            serializer = SelectedEquipmentSerializer(selected_id)
            # message = f'{user_obj.name} is not wearing {a}'
            message = "This employee did not wear personal protection equipment"
            message1 = "You did not confirm you wear personal equipment, but you are climbing up already"

            if length_key<17:
                """
                 sending Notification to employee
                """
                print("user obj", user_obj.employee_supervisor)
                if FCMDevice.objects.filter(user=user_obj).exists():
                    self.send_loggin_push_notification(user_obj, message)
                else:
                    result = {'code': status.HTTP_204_NO_CONTENT, 'message': "User Not Found!"}
                    
                if FCMDevice.objects.filter(user=user_obj.employee_supervisor).exists():
                    self.send_loggin_push_notification(user_obj.employee_supervisor, message)
                else:
                    result = {'code': status.HTTP_204_NO_CONTENT, 'message': "User Not Found!"}
                # try:
                #     self.send_loggin_push_notification(user_obj, message)
                #     self.send_loggin_push_notification(user_obj.employee_supervisor, message)
                # except:
                #     self.send_loggin_push_notification(user_obj, message)

            result = {'data': serializer.data, 'code': status.HTTP_200_OK, 'message': "Records Updated successfully!"}
        else:
            result = {'data': serializer.errors, 'code': status.HTTP_400_BAD_REQUEST, 'message': "FAIL"}
        return result


    def send_loggin_push_notification(self, user, message=None):
        from api.utils import send_push_notification

        # message = "This user is not wearing the equipments!"
    
        send_push_notification(False, None, user, message, None)