import requests
from django.db.models import Max
from django.urls import reverse
from requests.auth import HTTPBasicAuth

from client.models import Client, Region, ClientType, Sms
from order.models import WashOrder, Setting
from payment.models import ProjectSetting


def create_client(post_request, user_request):
    full_name = post_request.get('full_name', None)
    address = post_request.get('address', None)
    region = post_request.get('region', None)
    phone = post_request.get('phone', None)
    client_type = post_request.get('client_type', None)
    Client.objects.create(full_name=full_name,
                          phone=phone,
                          address=address,
                          region_id=region,
                          client_type_id=client_type)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'client-list')),
         'data': ''})


def delete_client(post_request, user_request):
    client_id = post_request.get('client_id', None)
    client = Client.objects.get(id=int(client_id))
    client.delete()
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'client-list')),
         'data': ''})


def create_region(post_request, user_request):
    name = post_request.get('name', None)
    Region.objects.create(name=name)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'region-list')),
         'data': ''})


def delete_region(post_request, user_request):
    region_id = post_request.get('region_id', None)
    region = Region.objects.get(id=int(region_id))
    region.delete()
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'region-list')),
         'data': ''})


def create_client_type(post_request, user_request):
    name = post_request.get('name', None)
    ClientType.objects.create(name=name)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'client-type-list')),
         'data': ''})


def delete_client_type(post_request, user_request):
    client_type_id = post_request.get('client_type_id', None)
    client_type = ClientType.objects.get(id=int(client_type_id))
    client_type.delete()
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'client-type-list')),
         'data': ''})


def create_wash_order_from_client_list(post_request, user_request):
    client_id = post_request.get('client_id', None)
    max_count = WashOrder.objects.all().aggregate(max_count=Max('numbering'))
    wash_order = WashOrder.objects.create(client_id=client_id,
                                          user_id=user_request.id,
                                          status='during',
                                          price=ProjectSetting.load().rate,
                                          numbering=1 if max_count['max_count'] is None else max_count['max_count'] + 1)

    return dict(
        {'back_url': reverse(post_request.get('back_url', 'wash-order-detail'), kwargs={'pk': wash_order.pk}),
         'data': ''})


def send_sms(to, text):
    try:
        sms = Sms.objects.create(msdsn=to, text=text)
        sms_id = f"alc{sms.id}"
        url = 'http://91.204.239.44/broker-api/send'
        data = {
            "messages": [
                {
                    "recipient": to,
                    "message-id": sms_id,
                    "sms": {
                        "originator": "3700",
                        "content": {
                            "text": str(text)
                        }
                    }
                }
            ]
        }
        headers = {'Content-Type': 'application/json'}

        r = requests.post(url, json=data,
                          headers=headers, auth=HTTPBasicAuth('login', 'password'))
        return r
    except Exception as ex:
        print(ex)
        return ex


def update_region(post_request, user_request):
    region_id = post_request.get('region_pk', None)
    name = post_request.get('name', None)
    Region.objects.filter(pk=region_id).update(name=name)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'region-list')),
         'data': ''})


def update_client_type(post_request, user_request):
    client_type_id = post_request.get('client_type_pk', None)
    name = post_request.get('name', None)
    ClientType.objects.filter(pk=client_type_id).update(name=name)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'client-type-list')),
         'data': ''})
