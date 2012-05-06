# -*- coding: utf-8 -*-
from django import forms

from models import InternMessage


class MsgForm(forms.ModelForm):
    class Meta:
        model = InternMessage
        fields = ("name", "email", "tel", "message", "type")
        widgets = {"type": forms.HiddenInput, "message": forms.Textarea}
