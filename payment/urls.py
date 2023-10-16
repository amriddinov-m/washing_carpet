from django.urls import path

from payment.views import ReportIncomePaymentsView
urlpatterns = [
    path('report-income/', ReportIncomePaymentsView.as_view(), name='report-income'),
]
