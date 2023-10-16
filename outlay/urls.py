from django.urls import path

from outlay.views import OutlayPaymentCreateView

urlpatterns = [
    path('outlay-create/', OutlayPaymentCreateView.as_view(), name='outlay-create')
]
