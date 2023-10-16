from django.contrib import admin

from payment.models import PaymentLog, Cashier, ProjectSetting


@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    pass


@admin.register(Cashier)
class CashierAdmin(admin.ModelAdmin):
    pass


@admin.register(ProjectSetting)
class ProjectSettingAdmin(admin.ModelAdmin):
    pass
