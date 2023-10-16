from django.urls import reverse

from worker.models import Worker


def create_worker(post_request, user_request):
    full_name = post_request.get('full_name', None)
    Worker.objects.create(full_name=full_name,
                          user=user_request)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'worker-list')),
         'data': ''})


def update_worker(post_request, user_request):
    worker_pk = post_request.get('worker_pk', None)
    full_name = post_request.get('full_name', None)
    Worker.objects.filter(pk=worker_pk).update(full_name=full_name)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'worker-list')),
         'data': ''})


def delete_worker(post_request, user_request):
    worker_id = post_request.get('worker_id', None)
    worker = Worker.objects.get(id=worker_id)
    worker.delete()
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'worker-list')),
         'data': ''})
