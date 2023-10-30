from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.


class Sale(models.Model):
    title = models.CharField(max_length=255, verbose_name="Краткий заголовок акции")
    text = models.CharField(max_length=255, verbose_name="Краткое описание акции")
    image = models.ImageField(upload_to="sales/images/%Y/%m/%d/", verbose_name="Картинка акции")
    context = RichTextField(verbose_name="Контент страницы")
    publish_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"
        

class SliderTop(models.Model):
    image = models.ImageField(upload_to="sliders/%Y/%m/%d/")
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Верхний слайдер"
        verbose_name_plural = "Верхние слайдеры"


class SliderTwo(models.Model):
    image = models.ImageField(upload_to="sliders/%Y/%m/%d/")
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Нижний слайдер"
        verbose_name_plural = "Нижние слайдеры"

class Partner(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="partners/images/%Y/%m/%d/")
    site = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Партнер"
        verbose_name = "Партнеры"
        
    def __str__(self):
        return self.name