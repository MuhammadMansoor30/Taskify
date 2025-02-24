import django_filters as filters
from taskify.models import WorkItem, Team

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