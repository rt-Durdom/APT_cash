from django.db import models
from django.conf import settings


EVENT_CHOICES = [
    ("birthday", "День рождения"),
    ("beersday", "День пива"),
    ("Longtime", "Долго невиделись"),
    ("other", "Другое"),
]


class Collect (models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='collects',
        verbose_name='Автор сбора',
    )
    name_collect = models.CharField(
        max_length=250,
        verbose_name='Название сбора',
    )
    event = models.CharField(
        max_length=50,
        choices=EVENT_CHOICES,
        default="other",
        verbose_name='Повод сбора',
    )
    description = models.TextField(
        verbose_name='Описание сбора',
        blank=True,
    )
    current_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Текущая сумма сбора',
        default=0,
    )
    target_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Целевая сумма сбора',
        default=0,
    )
    donors_count = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Количество доноров',
    )
    image = models.URLField(
        blank=True,
        verbose_name='Картинка сбора',
    )
    ends_collect = models.DateTimeField(
        verbose_name='Дата окончания сбора',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания сбора',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления сбора',
    )

    class Meta:
        verbose_name = 'Общий сбор'
        verbose_name_plural = 'Сборы'

    def __str__(self):
        return self.name_collect


class Payment(models.Model):
    collect = models.ForeignKey(
        Collect,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Общий сбор',
    )
    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Донор',
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Сумма платежа',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата платежа',
    )

    class Meta:
        verbose_name = 'Пожертвование'
        verbose_name_plural = 'Пожертвования'

    def __str__(self):
        return f'{self.donor}'