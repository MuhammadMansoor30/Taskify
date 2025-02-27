import django_filters as filters
from taskify.models import WorkItem, Team, Manager, Developer, Task

class WorkItemFilters(filters.FilterSet):
    status = filters.CharFilter(field_name='status', lookup_expr='exact')
    is_approved = filters.BooleanFilter(field_name='is_approved', lookup_expr='exact')
    name = filters.CharFilter(field_name='name', lookup_expr="icontains")

    class Meta:
        models = WorkItem
        fields = ['name', 'status', 'is_approved']

class TeamFilters(filters.FilterSet):
    manager = filters.CharFilter(field_name='manager', lookup_expr='exact')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        models = Team
        fields = ['name', 'manager']

class ManagerFilters(filters.FilterSet):
    department = filters.CharFilter(field_name='department', lookup_expr='icontains')

    class Meta:
        models = Manager
        fields = ['department']

class DeveloperFilters(filters.FilterSet):
    manager = filters.CharFilter(field_name='manager', lookup_expr='exact')
    team = filters.CharFilter(field_name='team', lookup_expr='exact')

    class Meta:
        models = Developer
        fields = ['manager', 'team']

class TaskFilters(filters.FilterSet):
    priority = filters.CharFilter(field_name='priority', lookup_expr='icontains')
    team = filters.CharFilter(field_name='team', lookup_expr='exact')
    is_completed = filters.CharFilter(field_name='is_completed', lookup_expr='exact')

    class Meta:
        models = Task
        fields = ['priority', 'team', 'is_completed']


# Utility Function to check if LoggedIn Person is Manager or Developer
def get_manager_or_developer(user):
    try:
        manager = Manager.objects.get(user__email=user.email)
    except Manager.DoesNotExist:
        manager = None

    try:
        developer = Developer.objects.get(user__email=user.email)
    except Developer.DoesNotExist:
        developer = None

    return manager, developer