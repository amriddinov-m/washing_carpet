from payment.models import ProjectSetting


def change_rate(post_request):
    new_rate = post_request.get('rate', 0)
    ProjectSetting.objects.update(rate=new_rate)
    return {'rate': new_rate}
