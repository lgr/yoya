from django.contrib import admin
from models import *


class UrlAdmin(admin.ModelAdmin):
    list_display = ["site", "url"]
    list_filter = ["site"]
    search_fields = ["url"]


admin.site.register(SiteInfo)
admin.site.register(ProcessedUrl, UrlAdmin)
