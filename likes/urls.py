from django.urls import path
from . import views

'''
Contains the URLs for the authors endpoints.

Preceding URL is /service/authors/{author_id}/{paths in urlpatterns}/
'''

urlpatterns = [
    path('posts/<uuid:post_id>/likes/', views.PostLikesView.as_view(), name="post-likes-list"),
    path('posts/<uuid:post_id>/comments/<uuid:comment_id>/likes/', views.CommentLikesView.as_view(), name="comment-likes-list"),
    path('liked/', views.AuthorLikedView.as_view(), name="author-liked-view")
]
