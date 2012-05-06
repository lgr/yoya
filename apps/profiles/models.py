from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from imagekit.models import ImageModel
import datetime
import os

from apps.publications.models import Publication
from settings import LANGUAGES


LANGS = [(a, _(b)) for (a, b) in LANGUAGES]

GENDERS = (
    ("M", _("Male")),
    ("F", _("Female")),
    ("U", _("Undefined"))
)

STATUSES = (
    ("ACT", _("Active")),
    ("DEL", _("Deleted")),
    ("BAN", _("Banned"))
)


def get_profilepic_upload_path(instance, filename):
    return os.path.join("profile_pics", "%06d" % instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=_("System user"))
    joined_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(_("Modification date"), auto_now=True)
    gender = models.CharField(max_length=4,
                              choices=GENDERS,
                              default="U",
                              blank=True,
                              verbose_name=_("Gender"))
    picture = models.ImageField(upload_to=get_profilepic_upload_path,
                                null=True,
                                blank=True,
                                verbose_name=_("New profile picture"))
    birth_date = models.DateField(null=True,
                                  blank=True,
                                  default=datetime.date(1990, 1, 1),
                                  verbose_name=_("Date of Birth"))
    status = models.CharField(max_length=4,
                              choices=STATUSES,
                              default="ACT",
                              blank=True,
                              verbose_name=_("User Status"))
    language = models.CharField(max_length=4,
                                null=True,
                                blank=True,
                                choices=LANGS,
                                verbose_name=_("Language"))
    rank = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.user.username

    def get_language(self):
        if self.language:
            return self.language
        else:
            return 'es'

    def is_moderator(self):
        return self.user.groups.filter(name='szefy').exists()

    def without_adverts(self):
        return bool(self.is_moderator()
                    or self.user.groups.filter(name='no_adverts').exists())

    def get_publications_stats(self):
        pubs = Publication.objects.filter(author=self.user)
        return {'total': pubs.count(),
                'accepted': pubs.filter(status__in=('ACC', 'PUB')).count(),
                'rejected': pubs.filter(status='REJ').count(),
                'waiting': pubs.filter(status='PDN').count(),
                'deleted': pubs.filter(status='DEL').count(),
                'front_page': pubs.filter(status='PUB').count()
                }


class Ranking(models.Model):
    date = models.DateTimeField(null=True, blank=False,
                                default=datetime.datetime.now().date())
    rank = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(Profile, null=True, blank=False)


@receiver(post_save, sender=User, dispatch_uid="user_saved")
def create_profile(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    created = kwargs.pop('created', False)
    if created:
        profile = Profile.objects.create(user=instance)
        profile.rank = profile.id
        profile.save()
