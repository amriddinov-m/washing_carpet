from django.contrib import admin

from outlay.models import CategoryOutlay, OutLay


@admin.register(CategoryOutlay)
class CategoryExpenseAdmin(admin.ModelAdmin):
    pass


@admin.register(OutLay)
class ExpenseAdmin(admin.ModelAdmin):
    pass
