from django.db import models
import uuid

from authors.models import CustomUser
from posts.models import Posts
from comments.models import Comments


"""-- Likes
Description:
PRIMARY KEY: indexes
FOREIGN KEYS: comment_id, author_id"""
class Likes(models.Model):
    comment_id = models.ForeignKey(Comments,on_delete=models.CASCADE, null=True, blank=True)
    author_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE) # Author who liked the post
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True, blank=True)

    context = models.CharField(max_length=200,editable=True)
    summary = models.CharField(max_length=100,editable=True)
    type = models.CharField(max_length=4,editable=True)
    object = models.CharField(max_length=250,editable=True)