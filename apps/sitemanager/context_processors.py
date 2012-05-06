from django.utils import translation
from django.conf import settings
from django.contrib.sites.models import Site
from apps.profiles.models import Profile
import random


def site_vars(request):
    """
    Enables request.current_language
    """
    current = translation.get_language()[:2]
    if current == 'pl':
        fb = 'pl_PL'
    elif current == 'es':
        fb = 'es_ES'
    else:
        fb = 'en_US'
    return {
            'site': Site.objects.get_current(),
            'current_language': current,
            'fb_language': fb,
            'fb_key': settings.FACEBOOK_APP_ID,
            'random3': random.randrange(1, 3, 1),
            'all_languages': [(a, b) for (a, b)
                              in settings.LANGUAGES if a != current]
            }
