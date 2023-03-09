from django.test import TestCase
from likes import *
from base import *
from authors import *
from posts import *

from django.urls import reverse,resolve
from rest_framework import status
import ast
import json

# Create your tests here.
class InboxTest(TestCase):

    def test_send_post_inbox_to_self(self):
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
        
        url = reverse("inbox-list",args=[str(userData["user_id"])])


        url_post = reverse("posts-list",args=[str(userData["user_id"])])
        post = self.client.post(url_post,content,'application/json')
        l = post.content.decode("utf-8")        
        mydata = json.loads(l)

        post_id = mydata["post_id"]

        inbox_content = {
                "author_id" : str(userData["user_id"]),
                "post_id" : str(post_id) 
        }

        inbox = self.client.post(url,inbox_content,'application/json')

        self.assertEquals(inbox.status_code,status.HTTP_200_OK)
        

    def test_send_comment_inbox_to_self(self):
        url_signup = reverse("signup")
        url_login = reverse("login")
        user = {
            "username": "User1",
            "password": "password123"
        }

        signup = self.client.post(url_signup,user,'application/json')
        login = self.client.post(url_login,user,'application/json')
        user_data = login.content.decode("utf-8") 
        userData = json.loads(user_data)

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
        url_post = reverse("posts-list",args=[str(userData["user_id"])])
        post = self.client.post(url_post,post_content,'application/json')
        l = post.content.decode("utf-8")        
        mydata = json.loads(l)

        post_id = mydata["post_id"]
        

        url_comment = reverse("comments-list",args=[str(userData["user_id"]),str(post_id)])        
        comment = self.client.post(url_comment ,content,'application/json')
        k = comment.content.decode("utf-8")  
        comment_data = json.loads(k)

        url = reverse("inbox-list",args=[str(userData["user_id"])])

        inbox_content = {
                "author_id" : str(userData["user_id"]),
                "comment_id" : str(comment_data["comment_id"]) 
        }

        inbox = self.client.post(url,inbox_content,'application/json')

        self.assertEquals(inbox.status_code,status.HTTP_200_OK)     