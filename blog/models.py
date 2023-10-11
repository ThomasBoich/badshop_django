from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    publish_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="blog/posts/images/%Y/%m/%d/")
    text = RichTextField()
    


    class Meta:
        verbose_name = f"Статья"
        verbose_name_plural = "Статьи"
    
    def __str__(self):
        return self.title