from django.contrib.auth import user_logged_in
from django.db import models
from django.dispatch import receiver
from django.utils import timezone

from users.models import CustomUser


# Create your models here.


# Модель для промокодов
class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="Промокод")
    valid_from = models.DateTimeField(verbose_name="Действителен с", null=True, blank=True)
    valid_to = models.DateTimeField(verbose_name="Действителен до", null=True, blank=True)
    seil = models.IntegerField(default=0, max_length=3, verbose_name="Скидка в %")
    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"

    def is_valid(self):
        now = timezone.now()
        return self.valid_from <= now <= self.valid_to


class BonusWallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='bonus_wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Balance')

    def __str__(self):
        return f'Bonus Wallet for {self.user.email}'


    class Meta:
        verbose_name = "Бонусный кошелёк"
        verbose_name_plural = "Бонусные кошельки"

@receiver(user_logged_in, sender=CustomUser)
def create_or_update_user_bonus_wallet(sender, request, user, **kwargs):
    try:
        bonus_wallet = user.bonus_wallet
    except BonusWallet.DoesNotExist:
        # Если бонусного кошелька у пользователя нет, создаем его
        BonusWallet.objects.create(user=user)