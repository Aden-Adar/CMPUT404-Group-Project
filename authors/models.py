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

class Following(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower')
    following_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='is_following')
    started_following = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(user__isnull=False) & models.Q(following_user__isnull=False), name='user_and_following_user_not_null'),
        ]
        
        ordering = ['-started_following']
    
    def __str__(self):
        return f'{self.user} is following {self.following_user}'

class FollowingRequest(models.Model):
    user_request = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='requester')
    follow_request_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='is_follow_request')
    
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(user_request__isnull=False) & models.Q(follow_request_user__isnull=False), name='user_request_and_follow_request_user_not_null'),
        ]
    
    def __str__(self):
        return f'{self.user_request} has requested to follow {self.follow_request_user}'