from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Pickup, Profile, UserSavedLocation

admin.site.register(User, UserAdmin)
admin.site.register(Pickup)
admin.site.register(Profile)
admin.site.register(UserSavedLocation)
