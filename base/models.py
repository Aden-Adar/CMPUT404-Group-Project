from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

from .manager import CustomUserManager
# Create your models here.

'''
-- Author model
Description: This is the model for each user within the social network
PRIMARY KEY: author_id
FOREIGN KEYS:
'''
class CustomUser(AbstractUser):
    username = models.CharField(max_length=200,unique=True) #This is the username
    email = None
    password = models.CharField(max_length=200)
    github = models.CharField(max_length=200)
    #profile_image = models.CharField(max_length=200) https://www.geeksforgeeks.org/imagefield-django-models/
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [username,password]    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    @property
    def is_active(self):
        return self.is_active
    
'''
-- Posts
Description: This is the post model that an Author can create
PRIMARY KEY: post_id
FOREIGN KEYS: author_id

class Posts(models.Model):
    class Visbility(models.TextChoices):
        PUBLIC = 'P'
        FRIENDS = 'F'
        PRIVATE = 'V'
        
    #Choices for visibility
    post_visbility = models.CharField(max_length=1,choices=Visbility.choices,default=Visbility.PRIVATE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    published = models.TimeField()
    content_type = models.CharField(max_length=200)
    title = models.CharField(max_length=200,editable=True)
    content = models.TextField(max_length=300,editable=True)
    unlisted = models.BooleanField(default=False)


-- Comments
Description: This is the model for a comment created by Author within a Posts
PRIMARY KEY: comment_id
FOREIGN KEYS: user, post

class Comments(models.Model):
    comment_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    parent_comment_id = models.IntegerField(default = (-1))
    content_type = models.CharField(max_length=200)
    published = models.TimeField()
    content = models.TextField(max_length=300,editable=True)


-- CommentLikes
Description:
PRIMARY KEY: indexes
FOREIGN KEYS: comment_id, author_id

class CommentLikes(models.Model):
    comment_id = models.ForeignKey(Comments,on_delete=models.CASCADE)
    #author_id = models.ForeignKey(Author,on_delete=models.CASCADE) # what is this refering to?
    like = models.BooleanField(default=False)
    indexes = [
        models.Index(fields=['comment_id','author_id'])
    ]


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
'''
