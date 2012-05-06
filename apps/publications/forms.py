# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _

from models import Publication, ImagePublication, URLPublication


class AddPublication(forms.ModelForm):
    url = forms.URLField(label=_("URL"), required=False)
    file = forms.FileField(label=_('Image'), required=False)

    class Meta:
        model = Publication
        fields = ("name", "source", "description", "language", "url", "file")
        widgets = {
            "description": forms.Textarea,
        }

    def clean(self):
        if not (bool(self.cleaned_data.get('url', False))
                ^ bool(self.cleaned_data.get('file', False))):
            raise forms.ValidationError(_(u'Did you forget to select the ' \
                                            'file to upload or to introduce ' \
                                            'a video URL?'))
        return self.cleaned_data

    def save(self, commit=True, status='PDN', author=None):
        pub = super(AddPublication, self).save(commit=False)
        url = self.cleaned_data.get('url', '').strip()
        file = self.cleaned_data.get('file')
        pub_type = None
        if file:
            pub_type = ImagePublication()
        elif url:
            pub_type = URLPublication()
            pub_type.url = url
        if commit and pub and pub_type:
            pub_type.name = pub.name
            pub_type.source = pub.source
            pub_type.description = pub.description
            pub_type.language = pub.language
            if author:
                pub_type.author = author
            if status:
                pub_type.status = 'PDN'
            pub_type.save()
            if file:
                pub_type.image.save(file.name, file)
        return pub_type
