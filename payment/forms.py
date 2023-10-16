from django import forms
from django.contrib.auth.models import User

from client.models import Car
from outlay.choices import PAYMENT_METHOD_CHOICES
from outlay.models import CategoryOutlay, OutLay
from worker.models import Worker


class IncomePaymentForm(forms.Form):
    payment_amount = forms.FloatField(label='Сумма возврата')
    comment = forms.CharField(label='Комментарии', required=False)
    payment_type = forms.ChoiceField(label='Тип оплаты', choices=PAYMENT_METHOD_CHOICES)
    payment_method = forms.ChoiceField(label='Метод оплаты', choices=PAYMENT_METHOD_CHOICES)


class OutlayPaymentForm(forms.Form):
    outlay_category = forms.ModelChoiceField(label='Категория расхода', queryset=CategoryOutlay.objects.all(),
                                             required=True)
    outlay_type = forms.ModelChoiceField(label='Причина', queryset=OutLay.objects.all(), required=True)
    worker = forms.ModelChoiceField(label='Сотрудник', queryset=Worker.objects.all(), required=True)
    car = forms.ModelChoiceField(label='Машина', queryset=Car.objects.all(), required=True)
    payment_amount = forms.FloatField(label='Сумма расхода')
    comment = forms.CharField(label='Комментарии', required=False)
    payment_method = forms.ChoiceField(label='Метод оплаты', choices=PAYMENT_METHOD_CHOICES)


class ReportOutcomeForm(forms.Form):
    outlay_category = forms.ModelChoiceField(label='Категория расхода', queryset=CategoryOutlay.objects.all(),
                                             required=True)
    worker = forms.ModelChoiceField(label='Сотрудник', queryset=User.objects.all(), required=False)
    car = forms.ModelChoiceField(label='Машина', queryset=Car.objects.all(), required=False)
