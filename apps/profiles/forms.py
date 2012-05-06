# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.forms.widgets import FileInput

from models import Profile


class EditUser(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('picture', 'gender', 'birth_date', 'language')
        widgets = {'picture': FileInput}
