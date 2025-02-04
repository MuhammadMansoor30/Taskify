from rest_framework import serializers
from taskify.models import Manager

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['id', 'full_name', 'experience', 'department']
    

    def create(self, validated_data):
        user = self.context.get('user')
        if not user:
            raise serializers.ValidationError("No User Provided")
        validated_data['user'] = user
        return Manager.objects.create(**validated_data)