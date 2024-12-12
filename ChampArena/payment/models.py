from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'),('Succeeded', 'Succeeded'),('Failed', 'Failed')],default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ${self.amount} - {self.status}"
