from django.urls import path

from frontend.views import LoginView, HomeView, OtherActionView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login-view'),
    path('other/action/', OtherActionView.as_view(), name='other_action'),
]
