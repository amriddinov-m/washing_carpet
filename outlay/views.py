from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from outlay.models import CategoryOutlay, OutLay
from payment.forms import OutlayPaymentForm
from payment.helpers import payment_outcome
from client.models import Car
from payment.models import PaymentLog
from worker.models import Worker


class OutlayPaymentCreateView(TemplateView):
    template_name = 'outlay-create-list.html'

    def get_context_data(self, **kwargs):
        context = super(OutlayPaymentCreateView, self).get_context_data(**kwargs)
        context['outlay_payment_form'] = OutlayPaymentForm
        context['outlay_categories'] = CategoryOutlay.objects.all()
        context['outlay_type'] = OutLay.objects.select_related('outlay_category').all()
        context['payment_logs'] = PaymentLog.objects.filter(payment_log_type='outcome').select_related('user').order_by(
            '-created')[:5]
        return context

    def post(self, request, **kwargs):
        value_outlay_category = self.request.POST.get('outlay_category', '')
        value_outlay_type = self.request.POST.get('outlay_type', '')
        value_outlay_worker = self.request.POST.get('worker', None)
        value_outlay_comment = self.request.POST.get('comment', '')
        value_outlay_amount = self.request.POST.get('payment_amount', '')
        value_outlay_amount_method = self.request.POST.get('payment_method', '')

        outlay_category = CategoryOutlay.objects.get(pk=value_outlay_category)
        outlay = OutLay.objects.get(pk=value_outlay_type)
        if outlay_category.category_type == 'worker':
            worker = Worker.objects.get(pk=value_outlay_worker)
            print(worker)
            payment_outcome(value_outlay_amount, value_outlay_amount_method,
                            value_outlay_comment,
                            self.request.user, True, 2, value_outlay_type,
                            outlay_name=outlay.outlay_category.name, worker=worker,
                            outlay_child=value_outlay_worker)
        else:
            payment_outcome(value_outlay_amount, value_outlay_amount_method,
                            value_outlay_comment,
                            self.request.user, True, 1, value_outlay_type,
                            outlay_name=outlay.outlay_category.name)
        return redirect(reverse('outlay-create'))

