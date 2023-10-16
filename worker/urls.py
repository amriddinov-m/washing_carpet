from django.urls import path

from worker.views import WorkersView, WorkerActionView, WorkerDetailView, ReportWorkerPaymentView

urlpatterns = [
    path('worker-list/', WorkersView.as_view(), name='worker-list'),
    path('worker-detail/<int:pk>/', WorkerDetailView.as_view(), name='worker-detail'),
    path('report-worker-payment/', ReportWorkerPaymentView.as_view(), name='report-worker-payment'),
    path('worker/action/', WorkerActionView.as_view(), name='worker_action')
]
