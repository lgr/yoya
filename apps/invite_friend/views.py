from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.context_processors import request
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import ugettext as _
from django.http import Http404, HttpResponse
from datetime import datetime

from models import *
from forms import *


def invitation(request):
    sender_known = request.user.is_authenticated()
    if request.method == "POST":
        form = InvitationForm(request.POST,
                              name_optional=sender_known)
        if form.is_valid():
            if sender_known:
                inviter = request.user
            else:
                inviter = None
            inv = create_invitation(email=form.cleaned_data['invitee_email'],
                                    name=form.cleaned_data['invitee_name'],
                                    inviter=inviter,
                                inviter_name=form.cleaned_data['inviter_name'])
            send_invitation(inv, form.cleaned_data['path'])
            return HttpResponse(_("Your friend was invited, thanks!"))
    else:
        if request.method == "GET":
            path = request.GET.get('path', '/')
        form = InvitationForm(initial={'path': path})
    return render_to_response("invite_friend/invite.html",
                              {'form': form, 'sender_known': sender_known},
                              context_instance=RequestContext(request))


def create_invitation(email, name='', inviter=None, inviter_name=''):
    kwargs = {'email': email,
              'name': name}
    if inviter:
        kwargs['inviter'] = inviter
    else:
        kwargs['inviter_name'] = inviter_name
    return EmailInvitation.objects.create(**kwargs)


def send_invitation(invitation=None, site_path='',
                    template='invite_friend/invitation_email.html'):
    if invitation is None:
        invitation = EmailInvitation.objects.filter(time_sent__isnull=True) \
                                                                .order_by('?')
        if invitation:
            invitation = invitation[0]
    elif type(invitation) is int:
        invitation = EmailInvitation.objects.get(invitation)
    if invitation:
        invitation.time_sent = datetime.now()
        context = {'domain': Site.objects.get_current().domain,
                   'html': False,
                   'title': "Yoya.es: Tienes un nuevo mensaje",
                   'sender': invitation.get_inviter(),
                   'site_path': site_path,
                   'recipient': invitation.name}
        email = EmailMultiAlternatives(
                                    from_email='invitaciones@yoya.es',
                                    subject=context['title'],
                                    body=render_to_string(template, context),
                                    to=(invitation.email,))
        context['html'] = True
        email.attach_alternative(render_to_string(template, context),
                                 "text/html")
        email.send()
        invitation.time_sent = datetime.now()
        invitation.save()
