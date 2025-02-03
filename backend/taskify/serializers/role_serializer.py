from rest_framework import serializers
from taskify.models import Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name', 'code_name', 'permissions'] 