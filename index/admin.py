from django.contrib import admin

# Register your models here.

from .models import *

class SaleAdmin(admin.ModelAdmin):
    list_display = ('title',)

class SliderTopAdmin(admin.ModelAdmin):
    list_display = ('title',)

class SliderTwoAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Sale, SaleAdmin)
admin.site.register(SliderTop, SliderTopAdmin)
admin.site.register(SliderTwo, SliderTwoAdmin)
admin.site.register(Partner)