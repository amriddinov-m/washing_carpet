from django.contrib import admin

from client.models import Region, ClientType, Client


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(ClientType)
class ClientTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass
