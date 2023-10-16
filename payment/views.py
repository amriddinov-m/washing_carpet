from django.contrib.auth.models import User
from django.db.models import Sum, Subquery, OuterRef, Count, Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from client.models import Car
from order.models import WashOrder, WashOrderItem, Team
from outlay.models import CategoryOutlay, OutLay
from payment.forms import OutlayPaymentForm
from payment.helpers import payment_outcome
from payment.models import PaymentLog


class ReportIncomePaymentsView(TemplateView):
    template_name = 'report_income_payments.html'

    def get_context_data(self, **kwargs):
        context = super(ReportIncomePaymentsView, self).get_context_data(**kwargs)
        startdate = self.request.GET.get('startdate', '')
        enddate = self.request.GET.get('enddate', '')
        context['startdate'] = startdate
        context['enddate'] = enddate
        if startdate and enddate:
            payments = PaymentLog.objects.filter(created__range=[startdate + " 00:00", enddate + " 23:59"]) \
                .select_related('user').order_by('-created')
            wash_order_totals = WashOrder.objects \
                .filter(created_at__range=[startdate + ' 00:00', enddate + ' 23:59']) \
                .aggregate(count=Count('pk', distinct='pk'),
                           items_count=Count('wash_order_item'),
                           total_area=Sum('wash_order_item__area'),
                           total_summa=Sum('wash_order_item__summa'))
            context['wash_order_totals'] = wash_order_totals
            context['report_payments'] = payments
            context['sum_amount'] = payments.filter(payment_log_type='outcome').aggregate(
                payment_cash_total_amount=Sum('amount',
                                              filter=Q(payment_method='cash')),
                payment_card_total_amount=Sum('amount',
                                              filter=Q(payment_method='card')))
            context['report_teams'] = Team.objects \
                .prefetch_related('wash_order') \
                .annotate(count_wash_order=Count('wash_order',
                                                 filter=Q(wash_order__created_at__range=
                                                          [startdate + " 00:00", enddate + " 23:59"])),
                          count_wash_order_item=Subquery(WashOrderItem.objects.select_related('wash_order__team') \
                                                         .filter(wash_order__team_id=OuterRef('pk'),
                                                                 wash_order__created_at__range=
                                                                 [startdate + " 00:00", enddate + " 23:59"]) \
                                                         .values('wash_order__team_id') \
                                                         .annotate(count=Count('pk')) \
                                                         .values('count')),
                          area_wash_order_item=Subquery(WashOrderItem.objects.select_related('wash_order__team') \
                                                        .filter(wash_order__team_id=OuterRef('pk'),
                                                                wash_order__created_at__range=
                                                                [startdate + " 00:00", enddate + " 23:59"]) \
                                                        .values('wash_order__team_id') \
                                                        .annotate(area=Sum('area')) \
                                                        .values('area')),
                          summa_wash_order_item=Subquery(WashOrderItem.objects.select_related('wash_order__team') \
                                                         .filter(wash_order__team_id=OuterRef('pk'),
                                                                 wash_order__created_at__range=
                                                                 [startdate + " 00:00", enddate + " 23:59"]) \
                                                         .values('wash_order__team_id') \
                                                         .annotate(summa=Sum('summa')) \
                                                         .values('summa'))) \
                .values('id',
                        'worker_name',
                        'count_wash_order',
                        'count_wash_order_item',
                        'area_wash_order_item',
                        'summa_wash_order_item')
        else:
            payments = PaymentLog.objects.order_by('-created').select_related('user')
            wash_order_totals = WashOrder.objects \
                .aggregate(count=Count('pk', distinct='pk'),
                           items_count=Count('wash_order_item'),
                           total_area=Sum('wash_order_item__area'),
                           total_summa=Sum('wash_order_item__summa'))
            context['wash_order_totals'] = wash_order_totals
            context['sum_amount'] = payments.filter(payment_log_type='outcome').aggregate(
                payment_cash_total_amount=Sum('amount',
                                              filter=Q(payment_method='cash')),
                payment_card_total_amount=Sum('amount',
                                              filter=Q(payment_method='card')))
            context['report_teams'] = Team.objects.prefetch_related('wash_order') \
                .annotate(count_wash_order=Count('wash_order'),
                          count_wash_order_item=Subquery(WashOrderItem.objects.select_related('wash_order__team') \
                                                         .filter(wash_order__team_id=OuterRef('pk')) \
                                                         .values('wash_order__team_id') \
                                                         .annotate(count=Count('pk')) \
                                                         .values('count')),
                          area_wash_order_item=Subquery(WashOrderItem.objects.select_related('wash_order__team') \
                                                        .filter(wash_order__team_id=OuterRef('pk')) \
                                                        .values('wash_order__team_id') \
                                                        .annotate(area=Sum('area')) \
                                                        .values('area')),
                          summa_wash_order_item=Subquery(WashOrderItem.objects.select_related('wash_order__team') \
                                                         .filter(wash_order__team_id=OuterRef('pk')) \
                                                         .values('wash_order__team_id') \
                                                         .annotate(summa=Sum('summa')) \
                                                         .values('summa'))) \
                .values('id',
                        'worker_name',
                        'count_wash_order',
                        'count_wash_order_item',
                        'area_wash_order_item',
                        'summa_wash_order_item')
            context['report_payments'] = PaymentLog.objects.select_related('user') \
                .order_by('-created')
        return context
