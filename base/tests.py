from django.test import TestCase
from authors.models import *
from django.urls import reverse,resolve
from rest_framework import status
from base.views import *


# Create your tests here.
class SignupLoginTest(TestCase):
    
    def setUp(self):
        CustomUser.objects.create(
            type= "author",
            id= "b7208318-fa45-4952-a759-7eb8bb21ee4f",
            url= "https://cmput404-group-project.herokuapp.com/service/authors/b7208318-fa45-4952-a759-7eb8bb21ee4f/",
            host= "cmput404-group-project.herokuapp.com",
            username= "practice2",
            github= "",
            profileImage= "https://www.cssscript.com/wp-content/uploads/2020/12/Customizable-SVG-Avatar-Generator-In-JavaScript-Avataaars.js-150x150.png"
        )

    #Signing up a user
    def test_signup(self):
        url = reverse("signup")
        print(url)
        user2_json = {           
            "username":"user1",
            "password":"user1"

        }

        signup = self.client.post(url,user2_json,'application/json')

        
        self.assertEquals(signup.status_code,status.HTTP_201_CREATED)
        self.assertEquals(resolve(url).func.view_class,CreateAccount)

 #Signing up with the same username
    def test_same_username(self):
        url = reverse("signup")
        user1 = {
            "username": "User1",
            "password": "password123"
        }
        user2 = {
            "username": "User1",
            "password": "password123"
        }
        
        signup = self.client.post(url,user1,'application/json')
        signup = self.client.post(url,user2,'application/json')

        self.assertEquals(user2["username"],user1["username"])
        
        self.assertEquals(signup.status_code,status.HTTP_400_BAD_REQUEST)

    #Successful Login
    def test_login(self):
        url_signup = reverse("signup")
        url_login = reverse("login")

        user = {
            "username": "User1",
            "password": "password123"
        }

        signup = self.client.post(url_signup,user,'application/json')
        login = self.client.post(url_login,user,'application/json')

        self.assertEquals(signup.status_code,status.HTTP_201_CREATED)
        self.assertEquals(login.status_code,status.HTTP_200_OK)

    

