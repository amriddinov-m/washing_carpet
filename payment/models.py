from django.contrib.auth.models import User
from django.db import models
from payment.choices import PAYMENT_METHOD_CHOICES, CASHIER_TYPE_CHOICES


class PaymentLog(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT,
                             verbose_name='Пользователь')
    amount = models.IntegerField(verbose_name='Цена')
    aor = models.BooleanField(default=False)
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    outcat = models.IntegerField(default=0)
    outlay = models.IntegerField(default=0)
    outlay_child = models.IntegerField(default=0)
    payment_method = models.CharField(max_length=255,
                                      verbose_name='Метод оплаты',
                                      choices=PAYMENT_METHOD_CHOICES,
                                      blank=True)
    payment_log_type = models.CharField(max_length=255, verbose_name='Расход/Доход')

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'


class Cashier(models.Model):
    amount = models.FloatField(default=0,
                               verbose_name='Сумма')
    payment_type = models.CharField(max_length=10,
                                    verbose_name='Тип валюты',
                                    choices=CASHIER_TYPE_CHOICES,
                                    default='uzs')

    def __str__(self):
        return '{}: {}'.format(self.amount, self.payment_type)

    class Meta:
        verbose_name = 'Касса'
        verbose_name_plural = 'Касса'


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class ProjectSetting(SingletonModel):
    rate = models.FloatField(default=0)

    def __str__(self):
        return str(self.rate)

    class Meta:
        verbose_name = 'Курс доллара'
        verbose_name_plural = 'Курс доллара'
