from django.contrib import admin
from taskify.models import Permission, Role, User, Team, Manager, Developer, Task

# Register your models here so that they can appear in the Django admin site.

admin.site.register(Permission)
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Team)
admin.site.register(Manager)
admin.site.register(Developer)
admin.site.register(Task)