from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class ContactMessage(models.Model):
    TOPIC_CHOICES = [
        ('general', 'General'),
        ('support', 'Support Request'),
        ('feedback', 'Feedback or Suggestions'),
        ('complaint', 'Complaint or Issue'),
    ]
    title = models.CharField(max_length=100 , default="champarena")
    first_name = models.CharField(max_length=64, verbose_name="First Name")
    last_name = models.CharField(max_length=64, verbose_name="Last Name")
    email = models.EmailField()
    message = models.TextField()
    topic = models.CharField(max_length=64,choices=TOPIC_CHOICES,default='general')
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Topic:{self.topic} - message:{self.message}"
