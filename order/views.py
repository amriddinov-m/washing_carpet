from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, UpdateView
from django.views.generic.base import View

from client.models import Client
from order.helpers import create_team, delete_team, create_wash_order, delete_wash_order, create_wash_order_item, \
    delete_wash_order_item, update_wash_order_item, update_team_and_status, order_payment, update_status_wash_order
from order.models import Team, WashOrder, WashOrderItem, Setting
from payment.models import PaymentLog


class TeamListView(TemplateView):
    template_name = 'team-list.html'

    def get_context_data(self, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        context['teams'] = Team.objects.all()
        return context


class TeamDetailView(TemplateView):
    template_name = 'team-detail.html'

    def get_context_data(self, **kwargs):
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        context['team'] = Team.objects.get(pk=kwargs['pk'])
        return context


class TeamUpdateView(UpdateView):
    template_name = 'team-update.html'
    model = Team
    fields = '__all__'

    def get_success_url(self):
        return reverse('team-list')


class WashOrderListView(TemplateView):
    template_name = 'wash-order-list.html'

    def get_context_data(self, **kwargs):
        context = super(WashOrderListView, self).get_context_data(**kwargs)
        context['teams'] = Team.objects.all()
        context['clients'] = Client.objects.select_related('region', 'client_type').all()
        # context['statuses'] = SettingStatus.objects.all()
        post_request = self.request.POST.get
        status = post_request('status', None)
        wash_orders = post_request('wash_order_name', '')
        if wash_orders:
            context['wash_orders'] = WashOrder.objects \
                .select_related('team', 'client', 'user') \
                .filter(Q(id__icontains=wash_orders) |
                        Q(client__full_name__icontains=wash_orders) |
                        Q(client__phone__icontains=wash_orders)).order_by('-created_at')
            context['search_value'] = wash_orders
        elif status:
            context['wash_orders'] = WashOrder.objects \
                .select_related('team', 'client', 'user') \
                .filter(status=status).order_by('-created_at')
            context['filter_status'] = status
        else:
            context['wash_orders'] = WashOrder.objects \
                .select_related('team', 'client', 'user') \
                .order_by('-created_at')
        return context

    def post(self, request):
        return render(request, self.template_name, self.get_context_data())


class WashOrderDetailView(TemplateView):
    template_name = 'wash-order-detail.html'

    def get_context_data(self, **kwargs):
        context = super(WashOrderDetailView, self).get_context_data(**kwargs)
        context['wash_order'] = WashOrder.objects.get(pk=kwargs['pk'])
        context['teams'] = Team.objects.all()
        # context['statuses'] = SettingStatus.objects.all()
        context['setting'] = Setting.objects.first()
        wash_order_items = WashOrderItem.objects.filter(wash_order_id=kwargs['pk'])
        context['wash_order_items'] = wash_order_items.order_by('-id')
        context['total'] = wash_order_items.aggregate(total_area=Sum('area'),
                                                      total_summa=Sum('summa'))
        context['payments'] = PaymentLog.objects.filter(outlay=kwargs['pk'], outcat=1)
        return context


class WashOrderUpdateView(UpdateView):
    template_name = 'wash-order-update.html'
    model = WashOrder
    fields = ['team', 'client', 'status', 'end_time']

    def get_success_url(self):
        back_url = self.request.GET.get('back_url', 'wash-order-list')
        back_pk = self.request.GET.get('pk', None)
        if back_pk:
            return reverse(back_url, kwargs={'pk': back_pk})
        else:
            return reverse(back_url)


class OrderActionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OrderActionView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        post_request = self.request.POST
        user_request = self.request.user
        action = post_request.get('action', None)
        print(action)
        actions = {
            'create_team': create_team,
            'delete_team': delete_team,
            'create_wash_order': create_wash_order,
            'delete_wash_order': delete_wash_order,
            'create_wash_order_item': create_wash_order_item,
            'delete_wash_order_item': delete_wash_order_item,
            'update_wash_order_item': update_wash_order_item,
            'update_team_and_status': update_team_and_status,
            'update_status_wash_order': update_status_wash_order,
            'order_payment': order_payment
        }
        response = actions[action](post_request, user_request)
        back_url = response['back_url']
        if action == 'update_status_wash_order' and response['status'] == 'submitted':
            return JsonResponse(response, safe=False)
        else:
            return redirect(back_url)
