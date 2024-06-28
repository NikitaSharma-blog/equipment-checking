from django.urls import path
from api.views import *

app_name = 'api'

urlpatterns = [

    path('equipments/', EquipmentListView.as_view(), name='equipmets'),
    path('login/', LoginView.as_view(), name='login'),
    path('selectedeqp/', SelectedEquipmentView.as_view(), name='selectedeqp'),
    path('userstatus/', UserStatusView.as_view(), name='userstatus')
]
