from django.contrib import admin
from models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "joined_time", "status", "language"]
    list_filter = ['user', ]
    search_fields = ["user__username"]


class RankingAdmin(admin.ModelAdmin):
    list_display = ["date", "rank", "user"]
    list_filter = ["date", "rank"]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Ranking, RankingAdmin)
