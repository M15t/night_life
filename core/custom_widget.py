from django.forms.widgets import ClearableFileInput, Input, CheckboxInput, FileInput
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode


class CustomClearableFileInputWidget(ClearableFileInput):
    initial_text = 'Link'
    clear_checkbox_label = 'Delete'

    def render(self, name, value, attrs=None):
        template = '%(input)s'
        data = {'input': None, 'url': None}
        data['input'] = super(CustomClearableFileInputWidget,
                              self).render(name, value, attrs)

        if hasattr(value, 'url'):
            ext = str(value).split('.')[-1]
            if ext in ['jpg', 'png', 'svg']:
                data['url'] = conditional_escape(value.url)
                template = '<div class="thumbnail" style="margin-bottom:10px"><a href="%(url)s" data-popup="lightbox">' + \
                    '<img src="%(url)s">' + '</a></div>' + '%(input)s'
            elif ext in ['mp3']:
                data['url'] = conditional_escape(value.url)
                template = '<audio class ="w-full" preload="none" controls ><source src="%(url)s" /></audio>' + \
                    '%(input)s'
            elif ext in ['mp4']:
                data['url'] = conditional_escape(value.url)
                template = '<video style="margin-bottom: 10px;" id="my-player" class="video-js vjs-16-9 vjs-big-play-centered" controls preload="none" data-setup="{fluid: true}">' \
                    '<source src="%(url)s" type="video/mp4"></source>' \
                    '</video>' + '%(input)s'

            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                data['clear_checkbox_name'] = conditional_escape(checkbox_name)
                data['clear_checkbox_id'] = conditional_escape(checkbox_id)
                data['clear'] = CheckboxInput().render(
                    checkbox_name, False, attrs={'id': checkbox_id})
                data['clear_checkbox_label'] = 'Delete'
                data['clear_template'] = self.template_with_clear % data

        return mark_safe(template % data)


class AdminImageWidget(ClearableFileInput):
    def render(self, name, value, attrs=None):
        data = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = '%(input)s'
        data['input'] = Input.render(self, name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            data['initial'] = (
                '<img src="%s" alt="%s" style="max-width: 100px; max-height: 100px; border-radius: 5px;" /><br/>' % (
                    escape(value.url), escape(force_unicode(value)))
            )
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                data['clear_checkbox_name'] = conditional_escape(checkbox_name)
                data['clear_checkbox_id'] = conditional_escape(checkbox_id)
                data['clear'] = CheckboxInput().render(
                    checkbox_name, False, attrs={'id': checkbox_id})
                data['clear_template'] = self.template_with_clear % data

        return mark_safe(template % data)
