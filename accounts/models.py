from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)   
    ufi = models.CharField(max_length=11, unique=True)             
    address = models.TextField()                                   

    def __str__(self):
        return self.user.username
