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
        
        print(login.data)
        content = {
                
            "type": "post",
            "title": "A Friendly post title about a post about web dev",
            "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
            "source": "http://lastplaceigotthisfrom.com/posts/yyyyy",
            "description": "This post discusses stuff -- brief",
            "contentType": "text/plain",
            "content": "Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun",
            "author": {
                "type": "author",
                "id": "e9077778-c25a-4f69-bc31-607450e39e08",
                "host": "http://127.0.0.1:5454/",
                "displayName": "Lara Croft",
                "url": "http://127.0.0.1:5454/authors/e9077778-c25a-4f69-bc31-607450e39e08/",
                "github": "http://github.com/laracroft"
            },
            "categories":["web","tutorial"],
            "comments": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
            "published": "2015-03-09T13:07:04+00:00",
            "visibility": "FRIENDS",
            "unlisted": "false"

            }

        user_data = login.content.decode("utf-8") 
        userData = json.loads(user_data)
        
        url = reverse("inbox-list",args=[str(login.data["user_id"])])#userData["user_id"]


        #url_post = reverse("posts-list",args=[str(userData["user_id"])])
        post = self.client.post(url,content,'application/json')
        """ l = post.content.decode("utf-8")        
        mydata = json.loads(l)

        post_id = mydata["post_id"]

        inbox_content = {
                "author_id" : str(userData["user_id"]),
                "post_id" : str(post_id) 
        }

        inbox = self.client.post(url,inbox_content,'application/json') """

        self.assertEquals(post.status_code,status.HTTP_200_OK)
        
 
    def test_send_comment_inbox_to_self(self):
         #Creating post
        url_signup = reverse("signup")
        url_login = reverse("login")
        user = {
            "username": "User1",
            "password": "password123"
        }

        signup = self.client.post(url_signup,user,'application/json')
        login = self.client.post(url_login,user,'application/json')
        
        print(login.data)
        content = {
            "type":"comment",
            "author":{
                "type":"author",
                "id":"e9077778-c25a-4f69-bc31-607450e39e08",
                "url":"http://127.0.0.1:5454/authors/e9077778-c25a-4f69-bc31-607450e39e08/",
                "host":"http://127.0.0.1:5454/",
                "displayName":"Greg Johnson",
                "github": "http://github.com/gjohnson",
                "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            },
            "comment":"Sick Olde English",
            "contentType":"text/markdown",
            "published":"2015-03-09T13:07:04+00:00",
            "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c"
}

        user_data = login.content.decode("utf-8") 
        userData = json.loads(user_data)
        
        url = reverse("inbox-list",args=[str(login.data["user_id"])])#userData["user_id"]


        #url_post = reverse("posts-list",args=[str(userData["user_id"])])
        post = self.client.post(url,content,'application/json')
        """ l = post.content.decode("utf-8")        
        mydata = json.loads(l)

        post_id = mydata["post_id"]

        inbox_content = {
                "author_id" : str(userData["user_id"]),
                "post_id" : str(post_id) 
        }

        inbox = self.client.post(url,inbox_content,'application/json') """

        self.assertEquals(post.status_code,status.HTTP_200_OK)   