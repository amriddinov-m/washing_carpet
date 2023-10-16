from django.db import models

from outlay.choices import OUTLAY_TYPE_CHOICES


class CategoryOutlay(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Название')
    category_type = models.CharField(max_length=255, verbose_name='Тип категории расхода',
                                     choices=OUTLAY_TYPE_CHOICES, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория расходов'
        verbose_name_plural = 'Категории расходов'


class OutLay(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Название')
    outlay_category = models.ForeignKey('outlay.CategoryOutlay',
                                        on_delete=models.CASCADE,
                                        related_name='outlay',
                                        verbose_name='Категория расхода',
                                        blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'
