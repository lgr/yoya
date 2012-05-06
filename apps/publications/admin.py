from django.contrib import admin
from models import *


class PublicationAdmin(admin.ModelAdmin):
    list_display = ["name", "author", "get_status_display"]
    list_filter = ["time_added", "status"]
    search_fields = ["name", "description"]


class PublicationVoteAdmin(admin.ModelAdmin):
    list_display = ["user", "date", "plus"]
    list_filter = ["date", "publication"]


admin.site.register(PublicationVote, PublicationVoteAdmin)
admin.site.register(ImagePublication, PublicationAdmin)
admin.site.register(URLPublication, PublicationAdmin)
