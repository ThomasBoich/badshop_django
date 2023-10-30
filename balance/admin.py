from django.contrib import admin

from balance.models import BonusWallet, PromoCode

# Register your models here.

admin.site.register(BonusWallet)
admin.site.register(PromoCode)