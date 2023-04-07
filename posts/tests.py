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
        #url = reverse("posts-list",args=["f8b2ba2c-e91c-4365-9ab2-8320ff9cbf1b"])
        url = "https://cmput404-group-project.herokuapp.com/service/authors/62a14b78-94cc-4e04-b58d-e9a32371ac59/posts/"
        print("login ", login.data)

        user_data = login.data

        #print("login2 ", user_data["user_id"]) access UUID

        content = {
    "type": "post",
    "title": "Klydes md",
    "id": "https://cmput404-group-project.herokuapp.com/service/authors/62a14b78-94cc-4e04-b58d-e9a32371ac59/posts/40c6e0fb-4c44-4606-8790-8e0375b5677a/",
    "source": "https://cmput404-group-project.herokuapp.com/create",
    "origin": "https://cmput404-group-project.herokuapp.com/service/authors/62a14b78-94cc-4e04-b58d-e9a32371ac59/posts/40c6e0fb-4c44-4606-8790-8e0375b5677a/",
    "description": "markdown",
    "content_type": "text/markdown",
    "content": "# BOLDED",
    "author": {
        "type": "author",
        "id": "https://cmput404-group-project.herokuapp.com/service/authors/62a14b78-94cc-4e04-b58d-e9a32371ac59/",
        "url": "https://cmput404-group-project.herokuapp.com/service/authors/62a14b78-94cc-4e04-b58d-e9a32371ac59/",
        "host": "cmput404-group-project.herokuapp.com",
        "displayName": "klyde",
        "github": "",
        "profileImage": "https://www.cssscript.com/wp-content/uploads/2020/12/Customizable-SVG-Avatar-Generator-In-JavaScript-Avataaars.js-150x150.png"
    },
    "categories": [
        "md"
    ],
    "count": 0,
    "comments": "https://cmput404-group-project.herokuapp.com/service/authors/62a14b78-94cc-4e04-b58d-e9a32371ac59/posts/40c6e0fb-4c44-4606-8790-8e0375b5677a/comments/",
    "comments_set": [],
    "published": "2023-04-05T03:35:32.891807+00:00",
    "visibility": "PUBLIC",
    "unlisted": "false",
    "post_id": "40c6e0fb-4c44-4606-8790-8e0375b5677a"
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
        #url = reverse("posts-list",args=["f8b2ba2c-e91c-4365-9ab2-8320ff9cbf1b"])
        url = "https://cmput404-group-project.herokuapp.com/service/authors/62a14b78-94cc-4e04-b58d-e9a32371ac59/posts/"
        print("login ", login.data)

        user_data = login.data

        #print("login2 ", user_data["user_id"]) access UUID

        content = {
            "type": "post",
            "title": "Klydes md",
            "id": "https://cmput404-group-project.herokuapp.com/service/authors/62a14b78-94cc-4e04-b58d-e9a32371ac59/posts/40c6e0fb-4c44-4606-8790-8e0375b5677a/",
            "source": "https://cmput404-group-project.herokuapp.com/create",
            "origin": "https://cmput404-group-project.herokuapp.com/service/authors/62a14b78-94cc-4e04-b58d-e9a32371ac59/posts/40c6e0fb-4c44-4606-8790-8e0375b5677a/",
            "description": "markdown",
            "content_type": "text/markdown",
            "content": "# BOLDED",
            "author": {
                "type": "author",
                "id": "https://cmput404-group-project.herokuapp.com/service/authors/62a14b78-94cc-4e04-b58d-e9a32371ac59/",
                "url": "https://cmput404-group-project.herokuapp.com/service/authors/62a14b78-94cc-4e04-b58d-e9a32371ac59/",
                "host": "cmput404-group-project.herokuapp.com",
                "displayName": "klyde",
                "github": "",
                "profileImage": "https://www.cssscript.com/wp-content/uploads/2020/12/Customizable-SVG-Avatar-Generator-In-JavaScript-Avataaars.js-150x150.png"
            },
            "categories": [
                "md"
            ],
            "count": 0,
            "comments": "https://cmput404-group-project.herokuapp.com/service/authors/62a14b78-94cc-4e04-b58d-e9a32371ac59/posts/40c6e0fb-4c44-4606-8790-8e0375b5677a/comments/",
            "comments_set": [],
            "published": "2023-04-05T03:35:32.891807+00:00",
            "visibility": "PUBLIC",
            "unlisted": "false",
            "post_id": "40c6e0fb-4c44-4606-8790-8e0375b5677a"
        }

        post = self.client.post(url,content,'application/json')

        url2 = "https://cmput404-group-project.herokuapp.com/service/authors/62a14b78-94cc-4e04-b58d-e9a32371ac59/posts/40c6e0fb-4c44-4606-8790-8e0375b5677a/"

        post = self.client.post(url2,content,'application/json')
    

    