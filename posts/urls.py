from django.urls import path
from . import views


urlpatterns = [
    path("", views.PostListView.as_view(), name="posts-list"),
    path("<uuid:post_id>/", views.PostDetailView.as_view(), name="post-detail"),
    path("<uuid:post_id>/image/", views.ImageView.as_view(), name="image-view"),
]
