from django.urls import path
from . import views


urlpatterns = [
    path("", views.PostListView.as_view(), name="posts-list"),
    path("<uuid:post_id>/", views.PostDetailView.as_view(), name="post-detail"),
]
