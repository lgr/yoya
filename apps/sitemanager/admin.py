from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from models import *

admin.site.unregister(User)

UserAdmin.list_display = ('username', 'email',
                          'last_login', 'date_joined', 'is_staff')

admin.site.register(User, UserAdmin)
admin.site.register(InternMessage)
