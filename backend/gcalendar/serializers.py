from rest_framework import serializers
from .models import Homework

class HomeworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Homework
        fields = ['name', 'estimated_completion_time', 'due_date']

    def create(self, validated_data):
        # Get the user from the context
        user = self.context['user']

        # Convert estimated_completion_time to seconds
        estimated_completion_time_minutes = validated_data.get('estimated_completion_time', 0)
        validated_data['estimated_completion_time'] = estimated_completion_time_minutes * 60  # Convert to seconds
        
        # Create a new Homework instance with the user
        return Homework.objects.create(user=user, **validated_data)