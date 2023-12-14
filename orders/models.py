from django.contrib.sessions.models import Session
from django.db import models

from balance.models import PromoCode
from items.models import CartItem
from users.models import CustomUser, Address


# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)
    items = models.ManyToManyField(CartItem, verbose_name='Корзина')
    total_price = models.IntegerField(verbose_name='Сумма заказа', blank=True, null=True)  # Общая сумма заказа
    date_created = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=240, blank=True, null=True, verbose_name='Комментарий к заказу')
    delivery_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Адрес доставки')

    STATUS_CHOICES = (
        ('OP', 'Оплачен'),
        ('DL', 'Доставлен'),
        ('NP', 'Не оплачен'),
        ('DD', 'Выполняется доставка'),
    )

    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='NP', verbose_name='Статус заказа', blank=True, null=True)


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"{self.user.email}, {self.status}"


class OrderStatus(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Статусы заказов'
        verbose_name_plural = 'Статусы заказов'


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_amount = models.IntegerField()
    payment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class AppliedPromoCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Примененный промокод'
        verbose_name_plural = 'Примененные промокоды'

class TransportCompany(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название организации')

    class Meta:
        verbose_name = 'Транспортная компания'
        verbose_name_plural = 'Транспортные компании'

    def __str__(self):
        return self.name