from rest_framework import serializers
from taskify.models import WorkItem

class WorkItemSerializer(serializers.ModelSerializer):
    is_approved = serializers.BooleanField(default=False)

    class Meta:
        model = WorkItem
        fields = ['id', 'name', 'file', 'status', 'is_approved', 'task']
    
    
    def create(self, validated_data):
        user = self.context.get('added_by')
        if not user:
            raise serializers.ValidationError("No User Found")
        validated_data['added_by'] = user
        return WorkItem.objects.create(**validated_data)
    