import json
from xml.dom import ValidationErr

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .models import Notification, User

from fcm_django.models import FCMDevice

def send_push_notification(content_available, sender, receiver, alert, mtype="Message"):
    print("push")
    payload = {"is_chat": (mtype == 'Message'), "type": mtype, "sound": "default"}
    if content_available:
        payload["content-available"] = 1
    if sender is not None:
        payload["sender"] = str(sender.id)

    json_body = {"platform": [0, 1], "badge": "+1", "msg": alert, "payload": payload}

    if receiver is not None:
        receiver = User.objects.get(id=receiver.id)
        json_body["alias"] = str(receiver.id)
        print(receiver.id)

    body = json.dumps(json_body)

    try:
        # headers = {'content-type': 'application/json',
        #            'x-pushbots-appid': settings.PUSHBOTS_SETTINGS["X_PUSHBOTS_APPID"],
        #            'x-pushbots-secret': settings.PUSHBOTS_SETTINGS["X_PUSHBOTS_SECRET"]
        #            }
        notification = Notification(sender=sender, message=alert, type=mtype)
        print("receiver notification", receiver)
        if receiver is not None:
            notification.receiver = receiver
        notification.save()
        
        # print('Push Notification Body - ', body)

        fcm_push(receiver, body, notification.pk)
        
    except Exception as e:
        raise ImproperlyConfigured(str(e))

   
"""This is used as new push notification via firebase"""
def fcm_push(receiver, payload, notification_id=None):
    
    print("In fcm_push")
    userInstance = receiver.pk

    title = "Electricity POC"
    body=''
    payload = json.loads(payload)
    data = payload["payload"]
    print(data)
    data['notification_id'] = notification_id
    # for 
    data["msg"] = '' 
    if "msg" in payload.keys():
        # body = payload["msg"]
        data["msg"] = payload["msg"]
        body = payload["msg"]
    for onekey in payload.keys():
        if onekey =='payload':
            continue
        data[onekey] = payload[onekey]
    # try:
        # print('body - ', body)
    print('data - ', data)
    print("my payload", payload)
    device = FCMDevice.objects.get(user=userInstance)
    print("device user", userInstance)
    print('device', device)
    push_response = device.send_message(body=body, title=title, data=data)

    print('push_response - ', push_response)

    # except Exception as e:
    #     print("Exception Occurred in FCM push :", str(e))
    
    if notification_id:
        # print("notification")
        try:
            notification = Notification.objects.get(pk=notification_id)
            notification.response_code = 201
            notification.save()
        except Notification.DoesNotExist:
            pass