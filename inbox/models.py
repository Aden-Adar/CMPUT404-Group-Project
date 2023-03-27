from django.db import models

from authors.models import *
from posts.models import Posts
from comments.models import Comments
from likes.models import Likes

class Inbox(models.Model):
    class Type(models.TextChoices):
        POST = 'post'
        COMMENT = 'comment'
        LIKE = 'like'

    post = models.ForeignKey(Posts, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, null=True, blank=True, on_delete=models.CASCADE)
    like = models.ForeignKey(Likes, null=True, blank=True, on_delete=models.CASCADE)
    follow_request = models.ForeignKey(FollowingRequest, null=True, blank=True, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
