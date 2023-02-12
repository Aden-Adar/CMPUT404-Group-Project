from django.db import models
import uuid
# Create your models here.

'''
-- User model
Description: This is the model for each user within the social network
PRIMARY KEY: id
FOREIGN KEY:
'''
class User(models.Model):
    userID = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=200)
    name =  models.CharField(max_length=200)
    password = models.CharField(max_length=200)


'''
-- Post model
Description: Model for a post created by User
PRIMARY KEY: postID
FOREIGN KEY: userID
'''
class Post(models.Model):
    postID = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    userID = models.ForeignKey(User,on_delete=models.CASCADE)
    public = models.BooleanField(default=True)
    content = models.CharField(max_length=500)
    likes = models.JSONField(userID)

'''
-- Comment Section model
Description: Acts as the parent comment within the post
PRIMARY KEY: ---
FOREIGN KEY: postID
'''
class CommentSection(models.Model):
    postID = models.ForeignKey(Post,on_delete=models.CASCADE)

'''
-- Comment model
Description: The actual comment of a user in a post
PRIMARY KEY: userID
FOREIGN KEY: parentID, userID
'''
class Comment(models.Model):
    parentID = models.ForeignKey(CommentSection,on_delete=models.CASCADE)
    content = models.TextField(editable=True)
    userID = models.ForeignKey(User, primary_key=True, on_delete=models.CASCADE)
    dateCreated = models.DateField()
    




