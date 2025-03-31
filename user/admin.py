from django.contrib import admin

from .models import UserProfile,OtherData

admin.site.register(UserProfile)
admin.site.register(OtherData)
