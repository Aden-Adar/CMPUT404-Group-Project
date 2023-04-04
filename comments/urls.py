from django.urls import path
from . import views

'''
Contains the URLs for the authors endpoints.

Preceding URL is /service/authors/{author_id}/posts/{post_id}/comments/{path in urlpatterns}/
'''

urlpatterns = [
    path("",views.CommentListView.as_view(), name="comments-list"),
    path("<uuid:comment_id>/",views.CommentDetailView.as_view(), name="comment-detail"),
]
