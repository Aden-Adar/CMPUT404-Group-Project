from django.urls import path
from . import views


urlpatterns = [
    path("",views.CommentListView.as_view(), name="comments-list"),
    path("<uuid:comment_id>/",views.CommentDetailView.as_view(), name="comment-detail"),
]
