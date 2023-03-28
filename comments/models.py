from django.db import models
import uuid

from authors.models import CustomUser
from posts.models import Posts


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
    post = models.ForeignKey(Posts, null=True, blank=True,  on_delete=models.CASCADE)
    parent_comment_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=200, choices=ContentType.choices, default=ContentType.PLAIN)
    published = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=301,editable=True)

    type = models.CharField(max_length=8,editable=True)
    id = models.CharField(max_length=250,editable=True)
