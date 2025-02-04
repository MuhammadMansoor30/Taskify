from rest_framework import serializers
from taskify.models import Task
from datetime import datetime, timedelta

class TaskSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'team', 'status', 'priority', 'assigned_to']
    

    def get_duration(self, obj):
        priority = obj.priority
        if priority == 'Low':
            return datetime.today() + timedelta(days=1)
        elif priority == 'Medium':
            return datetime.today() + timedelta(days=3)
        elif priority == 'High':
            return datetime.today() + timedelta(days=5)