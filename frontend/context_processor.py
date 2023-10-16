from client.models import ClientType
from payment.models import Cashier, ProjectSetting


def pages(request):
    return {
        'client_types': ClientType.objects.all(),
        'cashiers': Cashier.objects.order_by('-payment_type'),
        'ps': ProjectSetting.load(),
    }
