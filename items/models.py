from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User  # Для авторизованных пользователей
from django.contrib.sessions.models import Session  # Для неавторизованных пользователей
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from users.models import CustomUser


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название товара")
    image = models.ImageField(unique="items/%Y/%m/%d/", blank=True, null=True, verbose_name="Изображение товара")
    price = models.IntegerField(default=0, blank=True, null=True, verbose_name="Цена товара")
    discount = models.IntegerField(default=0, blank=True, null=True, verbose_name="Скидка")
    seil_price = models.IntegerField(default=0, blank=True, null=True, verbose_name="Цена со скидкой")
    rating = models.IntegerField(default=0, blank=True, null=True, verbose_name="Рэйтинг")
    text = RichTextField(blank=True, null=True, verbose_name="Описание товара")
    compound = RichTextField(blank=True, null=True, verbose_name="Состав товара")
    delivery = RichTextField(blank=True, null=True, verbose_name="Информация о доставке")
    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.CASCADE, verbose_name="Категория")
    brend = models.ForeignKey('Brend', blank=True, null=True, on_delete=models.CASCADE, verbose_name="Бренд")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

    # @property
    # def seil_price(self):
    #     return self.price - (self.price * self.discount / 100)
    def save(self, *args, **kwargs):
        if self.price is not None and self.discount is not None:
            self.seil_price = self.price - (self.price * self.discount / 100)
        else:
            self.seil_price = None
        super(Item, self).save(*args, **kwargs)

class Category(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name="Название категории")
    parent = models.ForeignKey(
        'self',  # Ссылка на этот же класс (Category)
        on_delete=models.CASCADE,  # Удалять подкатегории, если удалена родительская категория
        blank=True,
        null=True,
        verbose_name="Родительская категория",
    )
    image = models.ImageField(upload_to="categories/images/%Y/%m/%d/", blank=True, null=True)
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title

class CertificateImages(models.Model):
    photo = models.ImageField(upload_to='certificates/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"


class Brend(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="brends/images/%Y/%m/%d/")
    
    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name



class FavoriteItem(models.Model):
    user = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, blank=True, null=True, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, blank=True, null=True, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')