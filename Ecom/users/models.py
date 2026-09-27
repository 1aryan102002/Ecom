from django.db import models
from django.contrib.auth.models import User

# Extra fields for Django's built-in User, linked one-to-one (access via user.profile)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True)
    recovery_email = models.EmailField(blank=True)

    def __str__(self):
        return self.user.username
