from django.db import models

# Create your models here.
from authentication.models import User

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_topics  = models.JSONField(default=list, blank=True)
    preferred_sources = models.JSONField(default=list, blank=True)
    
    
    def __str__(self):
        return f"{self.user.email}'s preferences"