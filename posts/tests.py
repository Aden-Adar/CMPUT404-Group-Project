from django.test import TestCase
from posts.models import *
from posts.views import *
from base.urls import *

from django.urls import reverse,resolve
from rest_framework import status
# Create your tests here.

class PostsTest(TestCase):

    def test_post_list(self):
        url = reverse("posts-list",args=["f7b2ba2c-e91c-4365-9ab2-8320ff9cbf1b"])
        self.assertEquals(resolve(url).func.view_class,PostListView)

    def test_post_detail(self):
        url = reverse("post-detail",args=["f7b2ba2c-e91c-4365-9ab2-8320ff9cbf1a","edab1d32-d929-4eaf-8994-469b36af9911"])
        self.assertEquals(resolve(url).func.view_class,PostDetailView)
     
    def test_create_post(self):
        
        url_signup = reverse("signup")
        url_login = reverse("login")
        user = {
            "username": "User1",
            "password": "password123"
        }

        signup = self.client.post(url_signup,user,'application/json')
        login = self.client.post(url_login,user,'application/json')
        url = reverse("posts-list",args=["f8b2ba2c-e91c-4365-9ab2-8320ff9cbf1b"])
        
        content = {
            "title": "Title 1",
            "description": "Some content",
            "content_type": "text/plain",
            "content": "This is a test",
            "visibility": "PUBLIC",
            "unlisted": "false",
            
        }

        post = self.client.post(url,content,'application/json')
        self.assertEquals(post.status_code,status.HTTP_201_CREATED)