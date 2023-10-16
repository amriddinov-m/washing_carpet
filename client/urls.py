from django.urls import path

from client.views import ClientActionView, ClientListView, ClientDetailView, ClientUpdateView, \
    RegionListView, ClientTypeListView

urlpatterns = [
    path('client-list/', ClientListView.as_view(), name='client-list'),
    path('client-detail/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('client-update/<int:pk>/', ClientUpdateView.as_view(), name='client-update'),
    path('region-list/', RegionListView.as_view(), name='region-list'),
    path('client-type-list/', ClientTypeListView.as_view(), name='client-type-list'),
    path('client/action/', ClientActionView.as_view(), name='client_action'),
]
