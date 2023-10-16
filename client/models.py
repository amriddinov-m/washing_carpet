from django.contrib.auth.models import User
from django.db import models

from client.choices import STATUS_CLIENT_CHOICES


class Region(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class ClientType(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип клиента'
        verbose_name_plural = 'Типы клиентов'


class Client(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлено на',
                                      auto_now_add=True)
    full_name = models.CharField(max_length=255,
                                 verbose_name='Полное Имя')
    phone = models.CharField(max_length=255,
                             verbose_name='Телефон',
                             blank=True, null=True)
    phone_extra = models.CharField(max_length=255,
                                   verbose_name='Доп. телефон',
                                   blank=True, null=True)
    address = models.CharField(max_length=255,
                               verbose_name='Адрес')
    region = models.ForeignKey('Region',
                               on_delete=models.SET_NULL,
                               null=True, blank=True,
                               verbose_name='Регион')
    client_type = models.ForeignKey('ClientType',
                                    on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    verbose_name='Тип клиента')
    status = models.CharField(max_length=255,
                              verbose_name='Статус',
                              default='active',
                              choices=STATUS_CLIENT_CHOICES)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Клинет'
        verbose_name_plural = 'Клиенты'


class Car(models.Model):
    worker = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Сотрудник')
    car_number = models.CharField(max_length=255,
                                  verbose_name='Номер машины')

    def __str__(self):
        return str(self.car_number)

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'


class Sms(models.Model):
    msdsn = models.CharField(max_length=255)
    text = models.CharField(verbose_name='Текст', max_length=255)
    date = models.DateField(verbose_name='Время', auto_now_add=True)

    def __str__(self):
        return "user:{}|text:{}".format(self.msdsn, self.text)

    class Meta:
        verbose_name = 'СМС'
        verbose_name_plural = 'СМС'
