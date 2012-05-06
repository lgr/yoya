from django import forms
from django.utils.translation import ugettext as _


class InvitationForm(forms.Form):
    invitee_email = forms.EmailField(label=_("Friend's e-mail"))
    invitee_name = forms.CharField(label=_("Friend's name"),
                                   max_length=32, required=False)
    inviter_name = forms.CharField(label=_("Your name"), max_length=32)
    path = forms.CharField(widget=forms.HiddenInput(), max_length=255)

    def __init__(self, *args, **kwargs):
        name_optional = kwargs.pop('name_optional', False)
        super(InvitationForm, self).__init__(*args, **kwargs)
        if name_optional:
            self.fields['inviter_name'].required = False
