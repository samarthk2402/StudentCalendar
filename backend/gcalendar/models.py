from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Homework(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='homeworks', on_delete=models.CASCADE)
    estimated_completion_time = models.DurationField()
    due_date = models.DateTimeField()
    event_id = models.CharField(max_length=255, blank=True, null=True)
    event_ids = models.JSONField(default=list, blank=True, null=True)  # Store multiple event IDs as a list