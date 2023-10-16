from django.db.models import Subquery, OuterRef, Sum
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView

from payment.models import PaymentLog
from worker.helpers import create_worker, delete_worker, update_worker
from worker.models import Worker


class WorkersView(TemplateView):
    template_name = 'worker-list.html'

    def get_context_data(self, **kwargs):
        context = super(WorkersView, self).get_context_data(**kwargs)
        context['workers'] = Worker.objects.select_related('user').all()
        return context


class WorkerDetailView(TemplateView):
    template_name = 'worker-detail.html'

    def get_context_data(self, **kwargs):
        context = super(WorkerDetailView, self).get_context_data(**kwargs)
        context['worker'] = Worker.objects.get(pk=kwargs['pk'])
        return context


class ReportWorkerPaymentView(ListView):
    template_name = 'report_worker_outlay.html'
    model = PaymentLog
    context_object_name = 'report_worker_payments'

    def get_context_data(self, **kwargs):
        context = super(ReportWorkerPaymentView, self).get_context_data(**kwargs)
        worker = self.request.GET.get('worker', '')
        startdate = self.request.GET.get('startdate', None)
        enddate = self.request.GET.get('enddate', None)
        context['workers'] = Worker.objects.select_related('user').all()
        context['startdate'] = startdate
        context['enddate'] = enddate
        context['selected_worker'] = worker
        if startdate and enddate:
            payments = PaymentLog.objects.filter(created__range=[startdate + " 00:00", enddate + " 23:59"],
                                                 payment_log_type='income').select_related('user').order_by('-created')
            if worker and worker != 'all':
                payments = payments.filter(outcat=2, outlay_child=worker)
            context['sum_amount'] = payments.select_related('user').aggregate(total_summa=Sum('amount'))
        else:
            if worker and worker != 'all':
                payments = PaymentLog.objects.filter(outcat=2, outlay_child=worker) \
                    .select_related('user').order_by('-created')
                context['sum_amount'] = payments.aggregate(total_summa=Sum('amount'))
            else:
                context['sum_amount'] = PaymentLog.objects.order_by('-created')\
                    .select_related('user').aggregate(total_summa=Sum('amount'))
        return context

    def get_queryset(self):
        startdate = self.request.GET.get('startdate', '')
        enddate = self.request.GET.get('enddate', '')
        worker = self.request.GET.get('worker', 'all')
        if worker and worker != 'all':
            outlay_ids = Worker.objects.filter(pk=worker).values_list('id', flat=True)
        if startdate and enddate:
            if worker and worker != 'all':
                return PaymentLog.objects.filter(created__range=[startdate + " 00:00", enddate + " 23:59"],
                                                 outcat=2,
                                                 outlay_child__in   =outlay_ids) \
                    .annotate(worker_payment=Subquery(Worker.objects.filter(id=OuterRef('outlay_child'))
                                                      .select_related('user')
                                                      .values('full_name')[:1])).order_by('-created')
            else:
                return PaymentLog.objects.filter(created__range=[startdate + " 00:00", enddate + " 23:59"]) \
                    .annotate(worker_payment=Subquery(Worker.objects.filter(id=OuterRef('outlay_child'))
                                                      .select_related('user')
                                                      .values('full_name')[:1])).order_by('-created')
        else:
            if worker and worker != 'all':
                return PaymentLog.objects.filter(outcat=2, outlay_child__in=outlay_ids) \
                    .annotate(worker_payment=Subquery(Worker.objects.filter(id=OuterRef('outlay_child'))
                                                      .select_related('user')
                                                      .values('full_name')[:1])).order_by('-created')
            else:
                return PaymentLog.objects.annotate(
                    worker_payment=Subquery(Worker.objects.filter(id=OuterRef('outlay_child'))
                                            .select_related('user')
                                            .values('full_name')[:1])).order_by('-created')


class WorkerActionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(WorkerActionView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        post_request = self.request.POST
        user_request = self.request.user
        action = post_request.get('action', None)
        actions = {
            'create_worker': create_worker,
            'update_worker': update_worker,
            'delete_worker': delete_worker,
        }
        response = actions[action](post_request, user_request)
        back_url = response['back_url']
        if action == '':
            return JsonResponse(response, safe=False)
        else:
            return redirect(back_url)
