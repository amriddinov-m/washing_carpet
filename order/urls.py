from django.urls import path

from order.views import TeamListView, OrderActionView, TeamDetailView, TeamUpdateView, WashOrderListView, \
    WashOrderDetailView, WashOrderUpdateView

urlpatterns = [
    path('team-list/', TeamListView.as_view(), name='team-list'),
    path('team-detail/<int:pk>/', TeamDetailView.as_view(), name='team-detail'),
    path('team-update/<int:pk>/', TeamUpdateView.as_view(), name='team-update'),
    path('wash-order-list/', WashOrderListView.as_view(), name='wash-order-list'),
    path('wash-order-detail/<int:pk>/', WashOrderDetailView.as_view(), name='wash-order-detail'),
    path('wash-order-update/<int:pk>/', WashOrderUpdateView.as_view(), name='wash-order-update'),
    path('order/action/', OrderActionView.as_view(), name='order_action'),
]
