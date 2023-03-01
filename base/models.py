from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver

import uuid

from rest_framework.authtoken.models import Token
from .manager import CustomUserManager
# Create your models here.

'''
-- Author model
Description: This is the model for each user within the social network
PRIMARY KEY: author_id
FOREIGN KEYS:
'''
class CustomUser(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = None
    password = models.CharField(max_length=200)
    github = models.CharField(max_length=200)
    #profile_image = models.CharField(max_length=200) https://www.geeksforgeeks.org/imagefield-django-models/
    password = models.CharField(max_length=200)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["password"]    
    
    #assign the custom manager to the objects attribute
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
        

# -- Posts
# Description: This is the post model that an Author can create
# PRIMARY KEY: post_id
# FOREIGN KEYS: author_id

class Posts(models.Model):
    class Visibility(models.TextChoices):
        PUBLIC = 'PUBLIC'
        FRIENDS = 'FRIENDS'
        PRIVATE = 'PRIVATE'
    
    class ContentType(models.TextChoices):
        PLAIN = 'text/plain'
        MARKDOWN = 'text/markdown'
        BASE64 = 'application/base64'
        PNG = 'image/png;base64'
        JPEG = 'image/jpeg;base64'
    
    # Choices for visibility
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visibility = models.CharField(max_length=7,choices=Visibility.choices,default=Visibility.PRIVATE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=200, choices=ContentType.choices, default=ContentType.PLAIN)
    title = models.CharField(max_length=200,editable=True)
    description = models.CharField(max_length=200,editable=True)
    content = models.TextField(max_length=300,editable=True)
    unlisted = models.BooleanField(default=False)

class PrivatePostViewer(models.Model):
    post_id = models.OneToOneField(Posts, on_delete = models.CASCADE, unique=True)
    viewer_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)



""" -- Comments
Description: This is the model for a comment created by Author within a Posts
PRIMARY KEY: comment_id
FOREIGN KEYS: user, post """

class Comments(models.Model):
    class ContentType(models.TextChoices):
        PLAIN = 'text/plain'
        MARKDOWN = 'text/markdown'
        BASE64 = 'application/base64'
        PNG = 'image/png;base64'
        JPEG = 'image/jpeg;base64'
    #Use django auto-generated id
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    parent_comment_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=200, choices=ContentType.choices, default=ContentType.PLAIN)
    published = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=301,editable=True)


"""-- Likes
Description:
PRIMARY KEY: indexes
FOREIGN KEYS: comment_id, author_id"""

class Likes(models.Model):
    comment_id = models.ForeignKey(Comments,on_delete=models.CASCADE, null=True, blank=True)
    author_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE) # Author who liked the post
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True, blank=True)

'''
-- Followers
Description: Followers of a user
PRIMARY KEY: indexes
FOREIGN KEYS: author_id

class Followers(models.Model):
    author_id = models.ForeignKey(CustomUser,null=True, on_delete=models.CASCADE,related_name='author')
    follower_id = models.ForeignKey(CustomUser,null=True, on_delete=models.CASCADE,related_name='follower')
    indexes = [
        models.Index(fields=['author_id','follower_id'])
    ]
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

'''

class Images(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
