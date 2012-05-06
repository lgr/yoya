from django.db import models
from django.contrib.auth.models import User


class EmailInvitation(models.Model):
    time_added = models.DateTimeField(auto_now_add=True)
    time_sent = models.DateTimeField(null=True, blank=True, default=None)
    inviter = models.ForeignKey(User, blank=True, null=True)
    inviter_name = models.CharField(max_length=64, blank=True)
    email = models.EmailField()
    name = models.CharField(max_length=64, blank=True)

    def get_inviter(self):
        if self.inviter:
            return self.inviter.username
        else:
            return self.inviter_name

    def __unicode__(self):
        return self.email
