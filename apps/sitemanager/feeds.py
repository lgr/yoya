# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from apps.publications.models import Publication
from django.db.models import Sum, Count
import datetime


class EntriesFeed(Feed):
    title = "Yoya.es - Las mejores imagenes del internet. Cada día las nuevas."
    link = "/"
    description = "El canal con nuevas imágenes de yoya.es"

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_public_url()


class LatestEntriesFeed(EntriesFeed):

    def items(self):
        return Publication.objects.filter(status='PUB') \
                                            .order_by('-time_published')[:30]


class DlvritFeed(EntriesFeed):

    def items(self):
        last24 = datetime.datetime.now() - datetime.timedelta(hours=24)
        pubs = Publication.objects.filter(
                   status='PUB',
                   time_published__gte=last24
                   ).annotate(
                   positive_vote=Sum('publicationvote__plus'),
                   total_vote=Count('publicationvote')
               )
        for pub in pubs:
            try:
                pub.votes_constant += (2 * int(pub.positive_vote)
                                        - pub.total_vote)
            except:
                pass
        return pubs.order_by('-votes_constant')[:8]
