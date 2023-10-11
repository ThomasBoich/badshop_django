from django.forms.widgets import ClearableFileInput
from django.utils.html import format_html


class InlineImageWidget(ClearableFileInput):
    template_name = 'widgets/inline-image.html'

    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        input_html = super(InlineImageWidget, self).render(name, value, attrs=attrs, renderer=renderer)
        img = self.instance.photo if self.instance and self.instance.photo else ''

        if img:
            img_html = format_html('<img src="{}" width="100px" height="100px">', img.url)

            html = format_html('<div class="inline-image-widget">{}</div>', img_html)
            return html + input_html
        else:
            return input_html