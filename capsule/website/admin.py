from website.models import *
from django.contrib import admin

class UserProfileAdmin(admin.ModelAdmin):
   list_display = ('user',)

admin.site.register(UserProfile, UserProfileAdmin)
