from rest_framework import serializers
from taskify.models import Developer

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ['id', 'full_name', 'experience', 'skill_Set', 'manager', 'team']