from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from django.core.cache import cache
from django.core.context_processors import request
from django.core.mail import mail_admins
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Sum, Count
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import check_for_language, ugettext as _
import datetime

from apps.publications.models import Publication, PublicationVote
from models import *
from forms import MsgForm


def change_language(request, response, language):
    if language and check_for_language(language):
        if hasattr(request, 'session'):
            request.session['django_language'] = language
        elif not response is None:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)


def paginate(entries, page, entries_per_page=5, paginator_area=3):
    paginator = Paginator(entries, entries_per_page)
    nexts = []
    prevs = []
    try:
        p = paginator.page(page)
    except:
        p = paginator.page(1)
    if p.has_next():
        next = page
        for pa in range(paginator_area):
            next += 1
            if next <= paginator.num_pages:
                nexts.append(next)
            else:
                break
    if p.has_previous():
        prev = page
        for pa in range(paginator_area):
            prev -= 1
            if prev > 0:
                prevs.append(prev)
            else:
                break
    res = {
        'publications': p.object_list,
        'current': p.number,
        'show_paginator': paginator.num_pages > 1,
        'prevs': sorted(prevs),
        'nexts': nexts
    }
    if paginator.num_pages == p.number:
        res['last_page'] = True
    if paginator.num_pages > 1:
        res.update({
            'prevs_dots': bool(prevs and (min(prevs) > 2)),
            'nexts_dots': bool(nexts and ((max(nexts) + 1)
                                          < paginator.num_pages))
        })
    if nexts and paginator.num_pages > max(nexts):
        res['total'] = paginator.num_pages
    if prevs and min(prevs) > 1:
        res['first'] = 1
    return res


def start(request, active='index', page=1, template="index.html"):
    user = request.user
    context = {
        'active': active,
    }
    fresh_index = False
    if active == 'index':
        pubs = cache.get(active + '_publications')
        if not pubs:
            pubs = Publication.objects.filter(status='PUB') \
                                                .order_by('-time_published')
            cache.set(active + '_publications', pubs, 60)
            fresh_index = True
    if active == 'top':
        pubs = cache.get(active + '_publications')
        if not pubs:
            pubs = Publication.objects.filter(status='PUB').annotate(
                       positive_vote=Sum('publicationvote__plus'),
                       total_vote=Count('publicationvote')
                   )
            for pub in pubs:
                try:
                    pub.votes_constant += (2 * int(pub.positive_vote)
                                            - pub.total_vote)
                except:
                    pass
            pubs = pubs.order_by('-votes_constant')[:100]
            cache.set(active + '_publications', pubs, 300)
    if active == 'moderate' and user.get_profile().is_moderator():
        pubs = Publication.objects.filter(status='PDN').order_by('time_added')
    if active == 'waiting_room':
        pubs = Publication.objects.filter(status='ACC') \
                                                    .order_by('-time_accepted')

    context.update(paginate(pubs, int(page)))
    total_index_count = cache.get('total_index_count')
    if fresh_index or total_index_count is None:
        total_index_count = Publication.objects.filter(status='PUB').count()
        cache.set('total_index_count', total_index_count, 60)
    context['total_index_yoyas'] = total_index_count
    if user.is_authenticated():
        votes = PublicationVote.objects.filter(user=user,
                    publication__id__in=[p.id for p
                                         in context['publications']])
        for pub in context['publications']:
            try:
                vote = votes.get(publication=pub)
                if vote.plus:
                    pub.voted_positively = True
                else:
                    pub.voted_negatively = True
            except:
                pass
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))


def contact(request, type, template='contact.html'):
    sent = False
    if request.method == "POST":
        form = MsgForm(request.POST)
        if form.is_valid():
            msg = form.save()
            try:
                mail_admins("[Message on YoYa] " + msg.get_type_display(),
                            message=msg.message,
                            fail_silently=True)
            except:
                pass
            sent = True
    else:
        form = MsgForm(initial={'type': type})
    return render_to_response(template,
                              {'form': form, 'sent': sent},
                              context_instance=RequestContext(request))


def get_context_list(id=None):
    pubs = Publication.objects.filter(status='PUB').order_by('-time_published')
    if id:
        pubs = pubs.exclude(id=id)
    return paginate(pubs, 1)


def taringa(request, num=10, template='taringa.html'):
    def arg2date(d):
        if len(d) > 8:
            return datetime.datetime(
                            int(d[0:4]),
                            int(d[4:6]),
                            int(d[6:8]),
                            int(d[8:10]),
                            int(d[10:12]))
        else:
            return datetime.datetime(
                            int(d[0:4]),
                            int(d[4:6]),
                            int(d[6:8]))
    if request.method == "POST":
        selected = []
        for key, value in request.POST.items():
            try:
                val = int(key)
                print key, value
                selected.append(val)
            except:
                pass
        context = {'pubs': Publication.objects.filter(id__in=selected)}
    else:
        pubs = Publication.objects.filter(status__in=('PUB', 'ACC'),
                                          language__in=('nn', 'es'))
        if 'from_date' in request.GET:
            pubs = pubs.filter(
                        time_published__gte=arg2date(request.GET['from_date']))
        if 'to_date' in request.GET:
            pubs = pubs.filter(
                        time_published__lte=arg2date(request.GET['to_date']))
        pubs = pubs.order_by('?')[:int(num)]
        context = {'randoms': pubs}
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))


def set_language(request, lang_code):
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    response = HttpResponseRedirect(next)
    change_language(request, response, lang_code)
    return response
