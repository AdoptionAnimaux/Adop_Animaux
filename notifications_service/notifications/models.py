from django.db import models
from django.utils import timezone

class Notification(models.Model):
    user_id = models.IntegerField()
    animal_id = models.IntegerField(null=True, blank=True)
    event = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notification for user {self.user_id}"
