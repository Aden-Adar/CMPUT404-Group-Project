from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
import uuid

from base.manager import CustomUserManager


'''
-- Author model
Description: This is the model for each user within the social network
PRIMARY KEY: author_id
FOREIGN KEYS:
'''
class CustomUser(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = None
    password = models.CharField(max_length=200)
    github = models.CharField(max_length=200)
    # profile_image = models.CharField(max_length=200) https://www.geeksforgeeks.org/imagefield-django-models/
    password = models.CharField(max_length=200)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["password"]    
    
    #assign the custom manager to the objects attribute
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
