from django.test import TestCase
from comments.models import *
from likes.views import *
from authors.models import *
from posts.urls import *
from base.urls import *

from django.urls import reverse,resolve
from rest_framework import status
# Create your tests here.

class LikesTest(TestCase):

    def test_post_likes(self):
        url = reverse("post-likes-list",args=["f7b2ba2c-e91c-4365-9ab2-8320ff9cbf1a","edab1d32-d929-4eaf-8994-469b36af9911"])

        self.assertEquals(resolve(url).func.view_class,PostLikesView)

    def test_comment_likes(self):
        url = reverse("comment-likes-list",args=["f7b2ba2c-e91c-4365-9ab2-8320ff9cbf1a","edab1d32-d929-4eaf-8994-469b36af9911", "a6cd7002-6801-4627-a3a1-21cd8be9b69d"])
        self.assertEquals(resolve(url).func.view_class,CommentLikesView)


    def test_liked(self):
        url = reverse("author-liked-view", args=["f7b2ba2c-e91c-4365-9ab2-8320ff9cbf1a"])

        self.assertEquals(resolve(url).func.view_class,AuthorLikedView)
  
