from django.contrib import admin
from models import *


class EmailInvitationAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "time_sent"]
    search_fields = ["email", "name", "inviter_name"]

admin.site.register(EmailInvitation, EmailInvitationAdmin)
