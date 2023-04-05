from django.urls import path
from . import views

'''
Contains the URLs for the authors endpoints.

Preceding URL is /service/authors/{author_id}/posts/{paths in urlpatterns}/
'''

urlpatterns = [
    path("", views.PostListView.as_view(), name="posts-list"),
    path("<uuid:post_id>/", views.PostDetailView.as_view(), name="post-detail"),
    path("<uuid:post_id>/image/", views.ImagesView.as_view(), name="image-view"),
]
