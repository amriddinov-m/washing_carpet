from django.contrib.auth.models import User
from django.db import models


class Worker(models.Model):
    full_name = models.CharField(max_length=255,
                                 verbose_name='Ф.И.О')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
