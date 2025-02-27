from django.contrib import admin
from taskify.models import Permission, Role, User, Team, Manager, Developer, Task, WorkItem

# Register your models here so that they can appear in the Django admin site.

class WorkItemAdmin(admin.ModelAdmin):
    list_filter = ['status', 'added_by', 'is_approved']
    search_fields = ['name']

class UserAdmin(admin.ModelAdmin):
    list_filter = ['roles', 'is_staff', 'is_superuser']
    search_fields = ['email', 'username']

class PermissionAdmin(admin.ModelAdmin):
    search_fields = ['code_name', 'name']

class DeveloperAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email']
    list_filter = ['team', 'manager']

class TaskAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ['team', 'priority', 'is_completed']

class ManagerAdmin(admin.ModelAdmin):
    list_filter = ['department']

admin.site.register(Permission, PermissionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(Team)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Developer, DeveloperAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(WorkItem, WorkItemAdmin)   # Registering the class to apply filters to admin site as well.