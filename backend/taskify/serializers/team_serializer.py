from rest_framework import serializers
from taskify.models import Team, Manager

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        exclude = ['description', 'created_by']