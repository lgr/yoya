from django.db import models
from django.utils.translation import ugettext_lazy as _

URL_TYPES = (
    ("I", _("Single item")),
    ("L", _("List"))
)


class SiteInfo(models.Model):
    name = models.CharField(max_length=64, blank=False)
    url = models.URLField(verbose_name=_("Address URL"))
    last_list_counter = models.IntegerField(default=1)
    last_item_counter = models.IntegerField(default=1)

    def __unicode__(self):
        return self.name


class ProcessedUrl(models.Model):
    site = models.ForeignKey(SiteInfo)
    time_added = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_("Time added"))
    url = models.URLField(verbose_name=_("Address URL"))
    type = models.CharField(max_length=1, choices=URL_TYPES, default="I")
