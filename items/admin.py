from django.contrib import admin
from django.db import models

from items.models import Item, Category, Brend, CertificateImages, CartItem, Cart


class CertificateImageInline(admin.TabularInline):  # или `admin.TabularInline` для табличного представления
    model = CertificateImages
    extra = 1
# Register your models here.


class ItemAdmin(admin.ModelAdmin):
    inlines = (CertificateImageInline,)
    list_display = ('name', 'price')
    list_filter = ('name', 'price')
    exclude = ('seil_price',)
    search_fields = ('name', 'price')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)
    list_editable = ('title',)
    search_fields = ('title',)


admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
admin.site.register(CertificateImages)
admin.site.register(Brend)
admin.site.register(CartItem)
admin.site.register(Cart)