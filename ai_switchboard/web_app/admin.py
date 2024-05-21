from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from ..web_app.models import Camera

# Unregister the original User admin
admin.site.unregister(User)


# Create a new User admin
class CustomUserAdmin(UserAdmin):
    pass  # Add your custom admin options here


# Register the new User Admin
admin.site.register(User, CustomUserAdmin)

admin.site.register(Camera)
