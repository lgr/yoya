from django.db import models
from django.utils.translation import ugettext_lazy as _


MSG_TYPES = (
    ("CNT", _("Contact message")),
    ("ADV", _("Advertisement Request"))
)


class InternMessage(models.Model):
    name = models.CharField(max_length=64,
                            blank=False,
                            verbose_name=_("Name and surname or " \
                                           "the company name"))
    email = models.CharField(max_length=64,
                             blank=False,
                             verbose_name=_("E-mail address"))
    tel = models.CharField(max_length=11,
                           blank=True,
                           verbose_name=_("Telephone number"))
    message = models.CharField(max_length=640,
                               blank=False,
                               verbose_name=_("Message"))
    sent = models.DateTimeField(auto_now_add=True,
                                verbose_name=_("Time sent"))
    type = models.CharField(max_length=3,
                            choices=MSG_TYPES,
                            default="CNT",
                            blank=False,
                            verbose_name=_("Type"))

    def __unicode__(self):
        return self.name + " " + unicode(self.sent)


class InvitedUsers(models.Model):
    email = models.CharField(max_length=64, blank=False)
    sent = models.DateTimeField(blank=True)
    name = models.CharField(max_length=64, blank=True)
