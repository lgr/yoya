from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sitemaps import ping_google
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

import datetime
import re


LINK_REGEXES = {
    'youtube': re.compile(r"^(http://)?(www\.)?(youtube\.com/watch\?v=)" \
                          "?(?P<id>[A-Za-z0-9\-=_]{11})"),
}

LANGS = [(a, _(b)) for (a, b) in settings.LANGUAGES]
LANGS.insert(0, ('nn', _('Every language')))

STATUSES = (
    ("PDN", _("Pending for Acceptance")),
    ("ACC", _("Accepted")),
    ("REJ", _("Rejected")),
    ("DEL", _("Deleted")),
    ("PUB", _("Published on the Front Page"))
)


class Publication(models.Model):
    author = models.ForeignKey(User, verbose_name=_("Author"))
    status = models.CharField(max_length=4,
                              choices=STATUSES,
                              default="PDN",
                              blank=True,
                              verbose_name=_("Status"))
    time_added = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_("Time added"))
    time_accepted = models.DateTimeField(null=True,
                                         blank=True,
                                         default=None,
                                         verbose_name=_("Time accepted"))
    time_published = models.DateTimeField(null=True,
                                          blank=True,
                                          default=None,
                                          verbose_name=_("Time published"))
    name = models.CharField(max_length=64,
                            blank=True,
                            verbose_name=_("Name"))
    source = models.CharField(max_length=64,
                              blank=False,
                              verbose_name=_("Source"))
    description = models.CharField(max_length=200,
                                   blank=True,
                                   verbose_name=_("Description"))
    language = models.CharField(max_length=4,
                                blank=True,
                                default="nn",
                                choices=LANGS,
                                verbose_name=_("Language"))
    votes_constant = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    def get_likes(self):
        return self.publicationvote_set.filter(plus=True).count()

    def get_dislikes(self):
        return self.publicationvote_set.filter(plus=False).count()

    def get_votes(self):
        return (self.publicationvote_set.filter(plus=True).count()
                + self.votes_constant
                - self.publicationvote_set.filter(plus=False).count())

    def is_valid(self):
        try:
            try:
                if self.imagepublication:
                    return self.imagepublication.is_valid()
            except:
                if self.urlpublication:
                    return self.urlpublication.is_valid()
        except:
            return False

    def is_accessible_for_user(self, user):
        try:
            if user.get_profile().is_moderator():
                return True
        except:
            pass
        if self.status in ('ACC', 'PUB'):
            return True
        else:
            return False

    def get_public_url(self):
        return reverse('publication_show', args=[self.id])

    def get_absolute_url(self):
        return reverse('publication_show_alone', args=[self.id])


class PublicationVote(models.Model):
    plus = models.BooleanField(default=True)
    publication = models.ForeignKey(Publication)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)


class ImagePublication(Publication):
    image = models.ImageField(upload_to="publications/%Y%m%d",
                              null=True, blank=False, verbose_name=_("Image"))

    def is_valid(self):
        return True


class URLPublication(Publication):
    url = models.URLField(verbose_name=_("Address URL"))

    def is_valid(self):
        return bool(self.get_type())

    def get_type(self):
        for (type, rx) in LINK_REGEXES.items():
            if rx.match(self.url):
                return type
        return None

    def widget(self):
        if self.get_type() == 'youtube':
            return self.youtube_widget()
        return ''

    def youtube_id(self):
        match = LINK_REGEXES['youtube'].match(self.url)
        if not match:
            return ''
        return match.group('id')

    def youtube_widget(self):
        return "<IFRAME width=\"560\" height=\"315\" src=\"http://www." \
               "youtube.com/embed/%(id)s\" frameborder=\"0\" " \
               "allowfullscreen></IFRAME>" % {'id': self.youtube_id()}


@receiver(models.signals.post_save,
          sender=Publication, dispatch_uid="publication_saved")
def notify_google(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    if instance.status in ('ACC', 'PUB'):
        try:
            ping_google()
        except Exception:
            pass
