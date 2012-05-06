from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.context_processors import request
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from django.http import Http404

from apps.sitemanager.views import change_language
from forms import EditUser


def login_wrapper(request):
    response = login(request, 'registration/login.html')
    if request.user.is_authenticated():
        try:
            lang = request.user.get_profile().language
        except:
            lang = 'en'
        change_language(request, response, lang)
    return response


@login_required
def show(request, user_id=None, template="profile.html"):
    try:
        return render_to_response(template,
                        {'user': User.objects.get(pk=user_id).get_profile()},
                        context_instance=RequestContext(request))
    except:
        raise Http404


@login_required
def edit(request, template="profile_edit.html"):
    user = request.user.get_profile()
    context = {'user': user}
    if request.method == "POST":
        form = EditUser(request.POST, request.FILES, instance=user)
        if form.is_valid():
            profile = form.save()
            context['success'] = True
            change_language(request, None, profile.language)
    else:
        form = EditUser(instance=user)
    context['form'] = form
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))
