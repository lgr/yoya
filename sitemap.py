from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap
from apps.publications.models import Publication


class MainSection():

    def __init__(self, name):
        self.name = name

    def get_absolute_url(self):
        return reverse(self.name)


class PublicationSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6


class Published(PublicationSitemap):

    def items(self):
        return Publication.objects.filter(status='PUB')

    def lastmod(self, obj):
        return obj.time_published


class Waiting(PublicationSitemap):

    def items(self):
        return Publication.objects.filter(status='ACC')

    def lastmod(self, obj):
        return obj.time_added


class StaticSections(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return [MainSection(sect_name) for sect_name in(
            'index',
            'waiting_room',
            'top',
            'advertisement',
            'contact',
            'faq',
            'regulations'
        )]

sitemaps = {
    'mainpage': Published,
    'waiting': Waiting,
    'static': StaticSections
}
