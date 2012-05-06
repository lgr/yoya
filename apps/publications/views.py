from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.context_processors import request
from django.core.files import File
from django.utils import simplejson
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
import os
import datetime

from apps.sitemanager.views import get_context_list

from models import *
from forms import *

# maximum publications per day per user
MAX_PER_DAY = 3


def show(request, pub_id=None, active=None, with_context=False):
    if pub_id is None:
        return show_random(request)
    else:
        pub = get_object_or_404(Publication, pk=pub_id)
    if not pub.is_accessible_for_user(request.user):
        raise Http404
    if request.user.is_authenticated():
        pass
    context = {'single_pub': pub, 'fb_title': pub.name}
    if with_context:
        context.update(get_context_list(pub.id))
    if active:
        context['active'] = active
    return render_to_response("index.html", context,
                              context_instance=RequestContext(request))


def show_random(request):
    pub = None
    while not pub:
        pub = Publication.objects.filter(status__in=('ACC', 'PUB')) \
                                                                .order_by('?')
    if pub:
        pub = pub[0]
        return show(request, pub.id, 'random')
    else:
        raise Http404


def vote(request, pub_id=None, positive=False):
    user = request.user
    result = {'id': pub_id, 'votes': False}
    if user.is_authenticated():
        try:
            pub = Publication.objects.get(pk=pub_id)
            if pub.author != user:
                vote, created = PublicationVote.objects.get_or_create(
                                                            publication=pub,
                                                            user=user)
                vote.plus = positive
                vote.save()
                result['votes'] = pub.get_votes()
        except:
            pass
    else:
        result['login_required'] = True
    return HttpResponse(simplejson.dumps(result),
                        content_type='application/json')


def moderate(request, pub_id=None, accept=False, front_page=False):
    user = request.user
    result = {'id': pub_id}
    if user.is_authenticated():
        if user.get_profile().is_moderator():
            try:
                pub = Publication.objects.get(pk=pub_id)
                if accept:
                    pub.status = 'ACC'
                    pub.time_accepted = datetime.datetime.now()
                elif front_page:
                    pub.status = 'PUB'
                    pub.time_published = datetime.datetime.now()
                else:
                    pub.status = 'REJ'
                pub.save()
            except:
                pass
        else:
            result = None
    else:
        result['login_required'] = True
    return HttpResponse(simplejson.dumps(result),
                        content_type='application/json')


@login_required
def add_new(request):
    context = {'active': 'add'}
    if (not request.user.get_profile().is_moderator()
        and Publication.objects.filter(
                author=request.user,
                time_added__gte=datetime.datetime.now().date()) \
            .count() > MAX_PER_DAY):
        context = {'not_allowed': MAX_PER_DAY}
    if not 'not_allowed' in context:
        if request.method == "POST":
            form = AddPublication(request.POST, request.FILES)
            if form.is_valid():
                pub = form.save(author=request.user, status='PDN')
                context['success'] = True
        else:
            form = AddPublication(
                initial={'language': request.user.get_profile().get_language()}
            )
        if not ('success' in context or 'not_allowed' in context):
            context['form'] = form
    return render_to_response("publications/add.html", context,
                              context_instance=RequestContext(request))
