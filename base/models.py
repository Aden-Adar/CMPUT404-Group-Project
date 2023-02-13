from django.db import models
import uuid
# Create your models here.

'''
-- Author model
Description: This is the model for each user within the social network
PRIMARY KEY: author_id
FOREIGN KEYS:
'''
class Author(models.Model):
    author_ID = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=200)
    github = models.CharField(max_length=200)
    profile_image = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    username = models.CharField(max_length=200)

'''
-- Posts
Description: This is the post model that an Author can create
PRIMARY KEY: post_id
FOREIGN KEYS: author_id
'''
class Posts(models.Model):
    #Choices for visibility
    VISIBILITY_CHOICES = (('P','PUBLIC'),('F','FRIENDS'),('V','PRIVATE'))


    post_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    author_id = models.ForeignKey(Author,on_delete=models.CASCADE)
    published = models.TimeField()
    content_type = models.CharField(max_length=200)
    title = models.CharField(max_length=200,editable=True)
    content = models.TextField(max_length=300,editable=True)
    unlisted = models.BooleanField(default=False)
    visibility = models.CharField(max_length=50,choices=VISIBILITY_CHOICES) #Should it be editable?


'''
-- Comments
Description: This is the model for a comment created by Author within a Posts
PRIMARY KEY: comment_id
FOREIGN KEYS: author_id, post_id
'''
class Comments(models.Model):
    comment_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    parent_comment_id = models.IntegerField(default = (-1))
    content_type = models.CharField(max_length=200)
    published = models.TimeField()
    content = models.TextField(max_length=300,editable=True)

'''
-- CommentLikes
Description:
PRIMARY KEY: indexes
FOREIGN KEYS: comment_id, author_id
'''
class CommentLikes(models.Model):
    comment_id = models.ForeignKey(Comments,on_delete=models.CASCADE)
    author_id = models.ForeignKey(Author,on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    indexes = [
        models.Index(fields=['comment_id','author_id'])
    ]

'''
-- Followers
Description: Followers of a user
PRIMARY KEY: indexes
FOREIGN KEYS: author_id
'''
class Followers(models.Model):
    author_id = models.ForeignKey(Author,null=True, on_delete=models.CASCADE,related_name='author')
    follower_id = models.ForeignKey(Author,null=True, on_delete=models.CASCADE,related_name='follower')
    indexes = [
        models.Index(fields=['author_id','follower_id'])
    ]

