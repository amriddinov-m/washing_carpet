from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.base import View

from frontend.forms import LoginForm
from frontend.helpers import change_rate
from order.models import WashOrder


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['wash_orders'] = WashOrder.objects.filter(status='during') \
            .select_related('team', 'client')
        return context


class LoginView(TemplateView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if 'back_url' in request.POST:
                        return redirect(request.POST['back_url'])
                    return redirect(reverse('home'))
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')


class OtherActionView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OtherActionView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        post_request = self.request.POST
        action = post_request.get('action', None)
        actions = {
            'change_rate': change_rate,
        }
        response = actions[action](post_request)
        if action == 'change_rate':
            return JsonResponse(response, safe=False)
