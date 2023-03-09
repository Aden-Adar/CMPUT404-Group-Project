from django.test import TestCase
from comments.models import *
from comments.views import *
from authors.models import *
from posts.urls import *
from base.urls import *

from django.urls import reverse,resolve
from rest_framework import status
import json

# Create your tests here.
class CommentsTest(TestCase):

    def test_comments_list(self):
        url = reverse("comments-list",args=["f7b2ba2c-e91c-4365-9ab2-8320ff9cbf1a","edab1d32-d929-4eaf-8994-469b36af9911"])

        self.assertEquals(resolve(url).func.view_class,CommentListView)

    def test_comment_detail(self):
        url = reverse("comment-detail",args=["f7b2ba2c-e91c-4365-9ab2-8320ff9cbf1a","edab1d32-d929-4eaf-8994-469b36af9911","a6cd7002-6801-4627-a3a1-21cd8be9b69d"])

        self.assertEquals(resolve(url).func.view_class,CommentDetailView)

    def test_create_comment(self):
        

        url_signup = reverse("signup")
        url_login = reverse("login")
        user = {
            "username": "User1",
            "password": "password123"
        }

        signup = self.client.post(url_signup,user,'application/json')
        login = self.client.post(url_login,user,'application/json')
        

        post_content = {
            "title": "Title 1",
            "description": "Some content",
            "content_type": "text/plain",
            "content": "This is a test",
            "visibility": "PUBLIC",
            "unlisted": "false",
        }

        content = {
            "comment": "This is a comment",
            "content_type": "text/plain"
}
        url_post = reverse("posts-list",args=["21197f66-d233-4b96-8ce9-fe548ac700f2"])
        post = self.client.post(url_post,post_content,'application/json')
        
        l = post.content.decode("utf-8")        
        mydata = json.loads(l)

        post_id = mydata["post_id"]
        

        url = reverse("comments-list",args=["21197f66-d233-4b96-8ce9-fe548ac700f2",str(post_id)])        
        comment = self.client.post(url,content,'application/json')
        self.assertEquals(comment.status_code,status.HTTP_201_CREATED)