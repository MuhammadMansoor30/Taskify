from django.contrib import admin
from taskify.models import Permission, Role, User

# Register your models here so that they can appear in the Django admin site.

admin.site.register(Permission)
admin.site.register(User)
admin.site.register(Role)