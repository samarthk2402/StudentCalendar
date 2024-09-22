from rest_framework import serializers
from .models import Homework

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ['name', 'estimated_completion_time', 'due_date']

    def create(self, validated_data):
        # Get the user from the context
        user = self.context['request'].user
        # Create a new Homework instance with the user
        return Homework.objects.create(user=user, **validated_data)