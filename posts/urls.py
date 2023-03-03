from django.urls import path
from . import views


urlpatterns = [
    path("", views.PostView.as_view(), name="posts-list"),
    path("<uuid:post_id>/", views.PostView.as_view(), name="post-detail"),
]
