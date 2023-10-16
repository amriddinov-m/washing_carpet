from django.db import models
from django.contrib.auth.models import User

from order.choices import WASH_ORDER_STATUS_CHOICES, TEAM_STATUS_CHOICES


# class SettingStatus(models.Model):
#     name = models.CharField(max_length=255,
#                             verbose_name='Название')
#     style = models.CharField(max_length=255,
#                              blank=True, null=True,
#                              choices=STATUS_COLOR_CHOICES,
#                              verbose_name='Стиль статуса')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'Настройка статуса'
#         verbose_name_plural = 'Настройки статуса'


class Team(models.Model):
    worker_name = models.CharField(max_length=255,
                                   verbose_name='Имя работника')
    phone = models.CharField(max_length=255,
                             verbose_name='Телефон')
    car_numb = models.CharField(max_length=255,
                                verbose_name='Номер машиины')
    status = models.IntegerField(default=0,
                                 choices=TEAM_STATUS_CHOICES,
                                 verbose_name='Статус')

    def __str__(self):
        return '{} | {}'.format(self.worker_name, self.phone)

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'


class WashOrder(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата старта')
    end_time = models.DateField(verbose_name='Дата окончания',
                                blank=True, null=True)
    team = models.ForeignKey('Team',
                             on_delete=models.SET_NULL,
                             related_name='wash_order',
                             null=True, blank=True,
                             verbose_name='Команда')
    client = models.ForeignKey('client.Client',
                               on_delete=models.CASCADE,
                               verbose_name='Клиент')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    status = models.CharField(max_length=255,
                              choices=WASH_ORDER_STATUS_CHOICES,
                              verbose_name='Статус')
    price = models.FloatField(default=0,
                              verbose_name='Цена')
    total = models.IntegerField(verbose_name='Общая сумма',
                                default=0)
    numbering = models.IntegerField(verbose_name='Нумерация',
                                    unique=True)

    def __str__(self):
        return '{} | {}'.format(self.client, self.created_at)

    class Meta:
        verbose_name = 'Заказ стирки'
        verbose_name_plural = 'Заказы стирки'


class WashOrderItem(models.Model):
    wash_order = models.ForeignKey('WashOrder',
                                   on_delete=models.CASCADE,
                                   related_name='wash_order_item',
                                   verbose_name='Заказ стирки')
    x_size = models.FloatField(default=0)
    y_size = models.FloatField(default=0)
    area = models.FloatField(default=0)
    summa = models.IntegerField(verbose_name='Сумма',
                                default=0)

    def __str__(self):
        return '{} | ({}|{})'.format(self.wash_order, self.x_size, self.y_size)

    class Meta:
        verbose_name = 'Элемент заказа стирки'
        verbose_name_plural = 'Элементы заказа стирки'


class Setting(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Название')
    numb = models.IntegerField(default=0)

    def __str__(self):
        return '{}: {}'.format(self.name, self.numb)
