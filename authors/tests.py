from django.test import TestCase
from authors.models import *
from django.urls import reverse,resolve
from authors.views import *
from authors.urls import *

# Create your tests here.

class AuthorsTest(TestCase):
    def setUp(self):
        CustomUser.objects.create(
            username = "User1",
            password = "password123",
            github = "www.github.com/user1"
        )
        CustomUser.objects.create(
            username = "User2",
            password = "2ndpassword",
            github = "www.github.com/user2"
        )

    #Regular test for author
    def test_author(self):
        user1 = CustomUser.objects.get(username = "User1")
        user2 = CustomUser.objects.get(username = "User2")

        user1.save()
        user2.save()

        self.assertEquals(user1.password, "password123")
        self.assertEquals(user1.github, "www.github.com/user1")

        self.assertEquals(user2.password, "2ndpassword")
        self.assertEquals(user2.github, "www.github.com/user2")

    #URL test for single author
    def test_url_single(self):
        url_single = reverse("author-detail",args=["f7b2ba2c-e91c-4365-9ab2-8320ff9cbf1a"])#This is a random UUID

        self.assertEquals(resolve(url_single).func.view_class, SingleAuthorView)

    #URL test for all authors
    def test_url_all(self):
        url_all = reverse("author-list")
        print("This is url: ",url_all)
        self.assertEquals(resolve(url_all).func.view_class,AllAuthorView)