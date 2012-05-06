# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _

from apps.publications.models import ImagePublication


class PubForm(forms.ModelForm):
    image = forms.URLField(label=_("URL"),
                           required=True, widget=forms.HiddenInput)
    proxy = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ImagePublication
        fields = ("name", "source", "description", "language", "image",
                  "proxy", "votes_constant")

    def save(self, author):
        pub = super(PubForm, self).save(commit=False)
        pub.author = author
        return pub
