from django.contrib import admin
from .models import UserProfile, Follow
# user related.

admin.site.register(UserProfile)
admin.site.register(Follow)
