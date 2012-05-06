from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.context_processors import request
from django.core.files import File
from django.utils import simplejson
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from tools import *
from models import *
from forms import *

import random
import re


ACTIVE_SITES = ('sadistic', 'kwejk', 'jebzdzidy', 'kecyroumen')


@login_required
def start(request, site_id='', page=0, template="spider/list_candidates.html"):

    def get_crawled_site(site_id, just_items=False):
        crawler = eval('crawl_' + site_id)
        return crawler(request, context, template, just_items)

    context = {'active': 'spider', 'page': int(page)}
    if site_id == 'all':
        default_context = context.copy()
        all_context = context.copy()
        all_context['sites'] = []
        counter = 1
        for site in ACTIVE_SITES:
            content = get_crawled_site(site, just_items=True)
            if not 'PROXY_URL' in content:
                content['PROXY_URL'] = None
            for p in content['publications']:
                p['counter'] = counter
                counter += 1
            all_context['sites'].append(content)
            context = default_context.copy()
        return render_to_response(template,
                              all_context,
                              context_instance=RequestContext(request))
    elif site_id in ACTIVE_SITES and request.user.get_profile().is_moderator():
        return get_crawled_site(site_id)
    else:
        raise Http404


def crawl_sadistic(request, context, template, just_items=False):
    def get_gallery(page):
        wp = WebPage(gallery_url + str(page))
        wp.download()
        articles = wp.getByCss('article.images')
        found = []
        for art in articles:
            item = {}
            title = wp.getByCss('header h2 a', art)
            pict = wp.getByCss('.galeria a img', art)
            votes = wp.getByCss('header .header_beers', art)
            if title:
                item['name'] = title[0].text
            if pict:
                item['image'] = pict[0].get('src')
            if pict:
                try:
                    item['votes_constant'] = int(votes[0].text)
                except:
                    item['votes_constant'] = 0
            if ('image' in item
                and not site.processedurl_set \
                                        .filter(url=item['image']).exists()):
                found.append(item)
                ProcessedUrl.objects.create(site=site,
                                            url=item['image'],
                                            type='I')
        return found
    gallery_url = 'http://www.sadistic.pl/galeria/'
    items_per_page = 10
    site = SiteInfo.objects.get(name='sadistic')
    candidates = []
    page = site.last_list_counter
    while not candidates:
        candidates = get_gallery(page)
        page += items_per_page
    site.last_list_counter = page
    site.save()
    clean_proxy()
    for cd in candidates:
        cd['source'] = '-'
        if cd['image'][-3:] in ('jpg', 'peg'):
            df = DownloadFile(url=cd['image'], to_proxy=True)
            df.download()
            cd['proxy'] = df.getFileName()
        cd['form'] = PubForm(initial=cd)
    context.update({
        'source_site': 'Sadistic',
        'publications': candidates,
        'source_url': gallery_url + str(page - items_per_page),
        'PROXY_URL': settings.PROXY_URL
    })
    if just_items:
        return context
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))


def crawl_kwejk(request, context, template, just_items=False):
    def get_gallery(page):
        url = gallery_url + str(page)
        ProcessedUrl.objects.create(site=site, url=url, type='L')
        wp = WebPage(url)
        wp.download()
        pictures = wp.getByCss('.shot .content .media img')
        found = []
        for art in pictures:
            item = {}
            title = art.get('alt')
            pict = art.get('src')
            if title:
                item['name'] = title
            if pict:
                item['image'] = pict
            if ('image' in item
                and not site.processedurl_set \
                                        .filter(url=item['image']).exists()):
                found.append(item)
                ProcessedUrl.objects.create(site=site,
                                            url=item['image'],
                                            type='I')
        return found
    gallery_url = 'http://kwejk.pl/strona/'
    site = SiteInfo.objects.get(name='kwejk')
    page = site.last_list_counter
    candidates = []
    while not candidates:
        candidates = get_gallery(page)
        page += 1
    site.last_list_counter = page
    site.save()
    for cd in candidates:
        cd['source'] = '-'
        cd['votes_constant'] = random.randint(21, 39)
        cd['form'] = PubForm(initial=cd)
    context.update({
        'source_site': 'Kwejk',
        'publications': candidates,
        'source_url': gallery_url + str(page - 1)
    })
    if just_items:
        return context
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))


def crawl_jebzdzidy(request, context, template, just_items=False):
    def get_gallery(page):
        url = gallery_url + str(page)
        ProcessedUrl.objects.create(site=site, url=url, type='L')
        wp = WebPage(url)
        wp.download()
        pictures = wp.getByCss('.obrazki .obrazek a img')
        found = []
        for art in pictures:
            item = {}
            title = art.get('alt')
            pict = art.get('src')
            if title:
                item['name'] = title
            if pict:
                item['image'] = pict
            if ('image' in item
                and not site.processedurl_set \
                                        .filter(url=item['image']).exists()):
                found.append(item)
                ProcessedUrl.objects.create(site=site,
                                            url=item['image'],
                                            type='I')
        return found
    gallery_url = 'http://jebzdzidy.pl/strona/'
    site = SiteInfo.objects.get(name='jebzdzidy')
    page = site.last_list_counter
    candidates = []
    while not candidates:
        candidates = get_gallery(page)
        page += 1
    site.last_list_counter = page
    site.save()
    for cd in candidates:
        cd['source'] = 'jebzdzidy [punto] pl'
        cd['votes_constant'] = random.randint(21, 39)
        cd['form'] = PubForm(initial=cd)
    context.update({
        'source_site': 'Jeb z dzidy',
        'publications': candidates,
        'source_url': gallery_url + str(page - 1)
    })
    if just_items:
        return context
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))


def crawl_kecyroumen(request, context, template, just_items=False):
    gallery_url = 'http://kecy.roumen.cz/roumingShow.php'
    # match filename from URL:
    re_file = re.compile(r'[\w_.-]*?(?=[\?\#])|[\w_.-]*$')
    site = SiteInfo.objects.get(name='kecyroumen')
    if 'start' in request.GET:
        next = request.GET['start']
    else:
        try:
            last = site.processedurl_set.latest('time_added').url
            next = re_file.search(last).group()
        except:
            next = 'telefonne_cislo.jpg'
    next = '?file=' + next
    candidates = []
    for k in range(6):
        url = gallery_url + next
        wp = WebPage(url)
        wp.download()
        title = wp.getByCss('.roumingForumMessage strong')
        pict = wp.getByCss('td a img')
        next = wp.getByCss('span.roumingButton a')[3].get('href')
        likes = wp.getByCss('span.roumingButton a[href^=roumingLike]')
        try:
            positive = int(re.search(r'^\d+', likes[0].text).group())
        except:
            positive = 0
        try:
            negative = int(re.search(r'^\d+', likes[1].text).group())
        except:
            negative = 0
        if title:
            title = title[0].text
        if pict and len(pict) > 1:
            pict = pict[1].get('src')
        else:
            pict = pict[0].get('src')
        if pict and not site.processedurl_set.filter(url=url).exists():
            candidates.append({
                'name': title,
                'image': pict,
                'form': PubForm(initial={
                            'name': title,
                            'image': pict,
                            'source': 'kecy [punto] roumen [punto] cz',
                            'votes_constant': positive - negative
                        })
            })
            ProcessedUrl.objects.create(site=site, url=url, type='I')
    context.update({
        'source_site': 'Kecy Roumen',
        'publications': candidates,
        'source_url': gallery_url + next
    })
    if just_items:
        return context
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))


def add_remote(request):
    if request.user.get_profile().is_moderator() and request.method == "POST":
        pub = PubForm(request.POST)
        if pub.is_valid():
            try:
                author = Group.objects.get(name='fake'). \
                                                    user_set.order_by('?')[0]
            except:
                author = request.user
            proxy = pub.cleaned_data['proxy']
            if proxy:
                df = ProxyFile(proxy)
            else:
                df = DownloadFile(request.POST['image'])
                df.download()
            p = pub.save(author=author)
            p.image.save(df.getFileName(p.name), df.getFile())
            p.save()
            df.close()
            if 'kwejk_crop' in request.POST and df.file_ext != '.gif':
                df.cropForKwejk(p.image.file.name)
            return HttpResponse("OK")
        print pub
    raise Http404
