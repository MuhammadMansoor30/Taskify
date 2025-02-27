from rest_framework import serializers
from taskify.models import Task
from datetime import datetime, timedelta

class TaskSerializer(serializers.ModelSerializer):
    # duration = serializers.SerializerMethodField()
    is_completed = serializers.BooleanField(default=False) 

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'team', 'is_completed', 'priority', 'status', 'assigned_to', 'task_deadline']
    
    def to_representation(self, instance):
        user_name = instance.assigned_to.username
        instance_data = super().to_representation(instance)
        instance_data['user_name'] = user_name
        return instance_data
    
    # getting user name from the instance using user field and adding it to the final serializer response.

    def create(self, validated_data):
        user = self.context.get('created_by')

        if not user:
            raise serializers.ValidationError("No User Found for the given id")
        
        validated_data['created_by'] = user
        return Task.objects.create(**validated_data)
    
    # If we want to validate some fields like user or others and we dont want to pass it in the final serailizer response then we can use its create method and pass fields as a context to the serializer to validate them and create object based on those.

    # def get_duration(self, obj):
    #     priority = obj.priority
    #     if priority == 'Low':
    #         return datetime.today() + timedelta(days=1)
    #     elif priority == 'Medium':
    #         return datetime.today() + timedelta(days=3)
    #     elif priority == 'High':
    #         return datetime.today() + timedelta(days=5)
        