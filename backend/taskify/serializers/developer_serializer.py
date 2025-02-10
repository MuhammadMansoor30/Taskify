from rest_framework import serializers
from taskify.models import Developer

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ['id', 'full_name', 'experience', 'skill_set', 'manager', 'team']
    
    def create(self, validated_data):
        user = self.context.get('user')
        if not user:
            raise serializers.ValidationError("No User Provided")
        validated_data['user'] = user
        return Developer.objects.create(**validated_data)


# This create method is added so that we can pass in the user data from the view to serailzer for validtaion but dont include it in the final serializer data.
# This will only validate the data against user and not add it in the final response coming from the serializer. Same in Manager model as well.