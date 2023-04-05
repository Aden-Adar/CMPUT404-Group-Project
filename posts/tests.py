from django.test import TestCase
from posts.models import *
from posts.views import *
from base.urls import *

from django.urls import reverse,resolve
from rest_framework import status
import ast
import json
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

    def test_post_edit(self):
        #Creating post
        url_signup = reverse("signup")
        url_login = reverse("login")
        user = {
            "username": "User1",
            "password": "password123"
        }

        signup = self.client.post(url_signup,user,'application/json')
        login = self.client.post(url_login,user,'application/json')
        
        
        content = {
            "title": "Title 1",
            "description": "Some content",
            "content_type": "text/plain",
            "content": "This is a test",
            "visibility": "PUBLIC",
            "unlisted": "false",
            
        }

        user_data = login.content.decode("utf-8") 
        userData = json.loads(user_data)
        
        url = reverse("posts-list",args=[str(userData["user_id"])])

        post = self.client.post(url,content,'application/json')
        l = post.content.decode("utf-8")        
        mydata = json.loads(l)
        post_id = mydata["post_id"]
        

        
        new_content = {
            
            "type": "posts",
            "title": "new posts",
            "id": "URL WILL BE HERE SOON",
            "source": str(mydata["source"]),
            "origin": str(mydata["origin"]),
            "description": "qweqwe",
            "content_type": "text/plain",
            "content": "qweqwe",
            "author": {
                "type": "author",
                "id": str(userData["user_id"]),
                "username": "User1",
                "github": ""
            },
            "comments": str(mydata["comments"]),
            "comments_set": [],
            "published": str(mydata["published"]),
            "visibility": "PUBLIC",
            "unlisted": "false",
            "post_id": str(post_id)

        }

        new_url = reverse("post-detail",args=[str(userData["user_id"]),str(post_id)])
        edit = self.client.put(new_url,new_content,'application/json')
        self.assertEquals(edit.status_code,status.HTTP_200_OK)

    def test_post_delete(self):
        #Creating post
        url_signup = reverse("signup")
        url_login = reverse("login")
        user = {
            "username": "User1",
            "password": "password123"
        }

        signup = self.client.post(url_signup,user,'application/json')
        login = self.client.post(url_login,user,'application/json')
        
        
        content = {
            "title": "Title 1",
            "description": "Some content",
            "content_type": "text/plain",
            "content": "This is a test",
            "visibility": "PUBLIC",
            "unlisted": "false",
            
        }

        user_data = login.content.decode("utf-8") 
        userData = json.loads(user_data)
        
        url = reverse("posts-list",args=[str(userData["user_id"])])

        post = self.client.post(url,content,'application/json')
        l = post.content.decode("utf-8")        
        mydata = json.loads(l)
        post_id = mydata["post_id"]
        

        new_url = reverse("post-detail",args=[str(userData["user_id"]),str(post_id)])
        delete = self.client.delete(new_url,content,'application/json')
        self.assertEquals(delete.status_code,status.HTTP_204_NO_CONTENT)