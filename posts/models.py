from django.db import models
import uuid

from authors.models import CustomUser


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
    content = models.TextField(max_length=300,editable=True,null=True,blank=True)
    unlisted = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images',null=True,blank=True)


# class PrivatePostViewer(models.Model):
#     post_id = models.OneToOneField(Posts, on_delete = models.CASCADE, unique=True)
#     private_viewers_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)