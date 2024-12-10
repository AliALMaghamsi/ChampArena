from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ActivityName(models.Model):
    
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Activity(models.Model):
    
    name = models.ForeignKey(ActivityName, on_delete=models.CASCADE, related_name='activities')
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_activities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activity_date = models.DateTimeField()
    location = models.CharField(max_length=255)  # Optional descriptive address
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.activity_date.strftime('%Y-%m-%d')})"


class ActivityParticipant(models.Model):
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Joined', 'Joined'),
        ('Completed', 'Completed'),
    ]
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='participants')
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities_joined')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.participant.username} - {self.activity.name}"

