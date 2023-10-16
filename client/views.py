from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, UpdateView
from django.views.generic.base import View

from client.helpers import create_client, delete_client, create_region, delete_region, create_client_type, \
    delete_client_type, create_wash_order_from_client_list, update_region, update_client_type
from client.models import Client, Region, ClientType
from order.models import WashOrder


class ClientListView(TemplateView):
    template_name = 'client-list.html'

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        context['regions'] = Region.objects.all()
        context['client_types'] = ClientType.objects.all()
        post_request = self.request.POST.get
        search_client = post_request('name_or_phone_client', '')
        client_type_id = post_request('client_type_id', None)
        clients = Client.objects.select_related('region', 'client_type')
        if search_client:
            context['clients'] = clients.filter(
                Q(full_name__icontains=search_client) | Q(phone__icontains=search_client)).order_by('-created_at')
            context['search_value'] = search_client
        elif client_type_id:
            sort_clients = clients.filter(client_type_id=client_type_id).order_by('-created_at')
            client_type = ClientType.objects.get(id=client_type_id)
            context['clients'] = sort_clients
            context['search_value'] = client_type.name
        else:
            context['clients'] = clients.all().order_by('-created_at')
        return context

    def post(self, request):
        return render(request, self.template_name, self.get_context_data())


class ClientDetailView(TemplateView):
    template_name = 'client-detail.html'

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        client = Client.objects.get(pk=kwargs['pk'])
        context['client'] = client
        context['wash_orders'] = WashOrder.objects.filter(client_id=client.pk)
        return context


class ClientUpdateView(UpdateView):
    template_name = 'client-update.html'
    model = Client
    fields = ['full_name', 'phone', 'phone_extra', 'address', 'region', 'client_type', 'status']

    def get_success_url(self):
        return reverse('client-list')


class ClientTypeListView(TemplateView):
    template_name = 'client-type-list.html'

    def get_context_data(self, **kwargs):
        context = super(ClientTypeListView, self).get_context_data(**kwargs)
        context['client_types'] = ClientType.objects.all().order_by('-id')
        return context


class RegionListView(TemplateView):
    template_name = 'region-list.html'

    def get_context_data(self, **kwargs):
        context = super(RegionListView, self).get_context_data(**kwargs)
        context['regions'] = Region.objects.all().order_by('-id')
        return context


class ClientActionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ClientActionView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        post_request = self.request.POST
        user_request = self.request.user
        action = post_request.get('action', None)
        actions = {
            'create_client': create_client,
            'delete_client': delete_client,
            'create_region': create_region,
            'update_region': update_region,
            'delete_region': delete_region,
            'create_client_type': create_client_type,
            'update_client_type': update_client_type,
            'delete_client_type': delete_client_type,
            'create_wash_order_from_client_list': create_wash_order_from_client_list,
        }
        response = actions[action](post_request, user_request)
        back_url = response['back_url']
        if action == '':
            return JsonResponse(response, safe=False)
        else:
            return redirect(back_url)
