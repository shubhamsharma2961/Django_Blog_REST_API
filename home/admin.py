from django.contrib import admin
from home.models import Blog
from account.models import UserProfile

admin.site.register(Blog)
admin.site.register(UserProfile)
