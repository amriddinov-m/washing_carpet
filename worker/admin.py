from django.contrib import admin

from worker.models import Worker


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    pass
