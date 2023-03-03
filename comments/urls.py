from django.urls import path
from . import views


urlpatterns = [
    path("comments/",views.CommentView.as_view(), name="comments-list"),
    path("comments/<uuid:comment_id>/",views.CommentView.as_view(), name="comment-detail"),
]
