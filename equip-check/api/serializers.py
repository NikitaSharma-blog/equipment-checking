from api.models import *
from rest_framework import serializers


class UserLoginDetailSerializer(serializers.ModelSerializer):
    """
    Return the details of Login User. This serializer is belongs to user service "login_for_mobile" function.
    """

    class Meta(object):
        model = User
        fields = ('id', 'email', 'name', 'device_token', 'roles', 'employee_supervisor')


class EquipmentListSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Equipments
        fields = ('id', 'name', 'image', 'status')


class SelectedEquipmentSerializer(serializers.ModelSerializer):
    selected_equipment = EquipmentListSerializer(read_only=True, many=True)

    class Meta:
        model = SelectedEquipments
        fields = ('id', 'user_id', 'selected_equipment')

class UserStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'user_status')


class DeviceTokenSerializer(serializers.ModelSerializer):
    """
    Return the details of Login User. This serializer is belongs to user service "login_for_mobile" function.
    """

    class Meta(object):
        model = User
        fields = ('id', 'device_token')