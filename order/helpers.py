from datetime import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django.template import loader, Context
from django.urls import reverse

from client.helpers import send_sms
from order.models import Team, WashOrder, WashOrderItem
from payment.helpers import payment_income
from payment.models import ProjectSetting


def create_team(post_request, user_request):
    worker_name = post_request.get('worker_name', None)
    phone = post_request.get('phone', None)
    car_numb = post_request.get('car_numb', None)
    status = post_request.get('status', None)
    Team.objects.create(worker_name=worker_name,
                        phone=phone,
                        car_numb=car_numb,
                        status=status)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'team-list')),
         'data': ''})


def delete_team(post_request, user_request):
    team_id = post_request.get('team_id', None)
    team = Team.objects.get(id=int(team_id))
    team.delete()
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'team-list')),
         'data': ''})


def create_wash_order(post_request, user_request):
    team_id = post_request.get('team', None)
    client_id = post_request.get('client', None)
    status = post_request.get('status', None)
    end_time = post_request.get('end_time', None)
    setting_course = ProjectSetting.objects.get(pk=1)
    WashOrder.objects.create(team_id=int(team_id),
                             client_id=int(client_id),
                             status=status,
                             user=user_request,
                             end_time=end_time,
                             price=setting_course.rate)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'wash-order-list')),
         'data': ''})


def delete_wash_order(post_request, user_request):
    wash_order_id = post_request.get('wash_order_id', None)
    wash_order = WashOrder.objects.get(id=int(wash_order_id))
    wash_order.delete()
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'wash-order-list')),
         'data': ''})


def update_wash_order_total(pk, total):
    WashOrder.objects.filter(pk=pk).update(total=total)


def create_wash_order_item(post_request, user_request):
    x_size = post_request.get('x_size', None)
    y_size = post_request.get('y_size', None)
    area = post_request.get('area', None)
    summa = post_request.get('summa', None)
    wash_order_id = post_request.get('wash_order_pk', None)
    WashOrderItem.objects.create(wash_order_id=wash_order_id,
                                 x_size=x_size,
                                 y_size=y_size,
                                 area=area,
                                 summa=summa)
    wash_order_item_total_summa = WashOrderItem.objects.filter(wash_order_id=wash_order_id) \
        .aggregate(total_summa=Sum('summa'))
    update_wash_order_total(wash_order_id, wash_order_item_total_summa.get('total_summa', 0))
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'wash-order-detail'), kwargs={'pk': wash_order_id}),
         'data': ''})


def delete_wash_order_item(post_request, user_request):
    wash_order_item_id = post_request.get('wash_order_item_id', None)
    wash_order_id = post_request.get('wash_order_id', None)
    wash_order_item = WashOrderItem.objects.get(id=int(wash_order_item_id))
    wash_order_item.delete()
    wash_order_item_total_summa = WashOrderItem.objects.filter(wash_order_id=wash_order_id) \
        .aggregate(total_summa=Sum('summa'))
    update_wash_order_total(wash_order_id, wash_order_item_total_summa.get('total_summa', 0))
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'wash-order-detail'), kwargs={'pk': wash_order_id}),
         'data': ''})


# def search_order_from_anywhere(post_request, user_request):
#     wash_orders = post_request.get('wash_order_name', '')
#     template = loader.get_template('wash-order-list.html')
#     context = Context({'wash_orders': wash_orders, })
#     return HttpResponse(template.render(context))


def update_wash_order_item(post_request, user_request):
    wash_order_item_id = post_request.get('wash_order_item_pk', None)
    wash_order_pk = post_request.get('wash_order_pk', None)
    x_size = post_request.get('x_size', None).replace(',', '.')
    y_size = post_request.get('y_size', None).replace(',', '.')
    area = post_request.get('area', None).replace(',', '.')
    summa = post_request.get('summa', None).replace(u'\xa0', '')
    WashOrderItem.objects.filter(pk=wash_order_item_id).update(x_size=float(x_size),
                                                               y_size=float(y_size),
                                                               area=float(area),
                                                               summa=int(summa))
    wash_order_item_total_summa = WashOrderItem.objects.filter(wash_order_id=wash_order_pk) \
        .aggregate(total_summa=Sum('summa'))
    update_wash_order_total(wash_order_pk, wash_order_item_total_summa.get('total_summa', 0))
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'wash-order-detail'), kwargs={'pk': wash_order_pk}),
         'data': ''})


def update_team_and_status(post_request, user_request):
    pk = post_request.get('wash_order_pk', None)
    wash_order = WashOrder.objects.get(pk=pk)
    team_value = post_request.get('team_value', None)
    WashOrder.objects.filter(pk=pk).update(team_id=team_value if team_value != '' else wash_order.team_id)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'wash-order-detail'), kwargs={'pk': pk}),
         'data': ''})


def update_status_wash_order(post_request, user_request):
    pk = post_request.get('wash_order_pk', None)
    wash_order = WashOrder.objects.get(pk=pk)
    status_value = post_request.get('status_value', None)
    wash_order_items = WashOrderItem.objects.filter(wash_order_id=wash_order.pk).aggregate(total_summa=Sum('summa'))
    if status_value == 'accepted':
        send_sms(wash_order.client.phone,
                 'Ваш заказ №{} принят, итоговая сумма {} сум'.format(wash_order.numbering,
                                                                      wash_order_items['total_summa']))
    WashOrder.objects.filter(pk=pk).update(status=status_value,
                                           end_time=datetime.now().date() if status_value == 'completed' else None)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'wash-order-detail'), kwargs={'pk': pk}),
         'status': status_value})


def order_payment(post_request, user_request):
    wash_order_pk = post_request.get('wash_order_pk', None)
    wash_order = WashOrder.objects.get(pk=wash_order_pk)
    value_outlay_amount = post_request.get('amount', 0)
    value_outlay_comment = post_request.get('comment', '')
    value_outlay_amount_method = post_request.get('payment_method', '')
    payment_income(value_outlay_amount, value_outlay_amount_method, value_outlay_comment, user_request,
                   True, 1, wash_order.pk, order_pk=wash_order_pk)
    send_sms(wash_order.client.phone,
             'Ваша оплата в сумме {} сум,по заказу №{} было принято'.format(value_outlay_amount,
                                                                            wash_order.numbering))
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'wash-order-detail'), kwargs={'pk': wash_order.pk}),
         'data': ''})
