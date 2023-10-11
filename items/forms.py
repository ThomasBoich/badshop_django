from django.forms import ModelForm, forms, widgets

from items.models import Item, CertificateImages


class AddItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


class ItemImageForm(forms.Form):

    photos = forms.FileField(widget=widgets.FileInput(attrs={'multiple': True}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ItemImageForm, self).__init__(*args, **kwargs)

    def clean_photos(self):
        # Остаются только картинки
        photos = [photo for photo in self.request.FILES.getlist('photos') if 'image' in photo.content_type]
        # Если среди загруженных файлов картинок нет, то исключение
        if len(photos) == 0:
            raise forms.ValidationError(u'Not found uploaded photos.')
        return photos

    def save_for(self, advert):
        for photo in self.cleaned_data['photos']:
            CertificateImages(photo=photo, advert=advert).save()