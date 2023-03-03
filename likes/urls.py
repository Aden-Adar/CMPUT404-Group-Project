from django.urls import path
from . import views


urlpatterns = [
    path('likes/', views.PostLikesView.as_view(), name="post-likes-list"),
    path('comments/<uuid:comment_id>/likes/', views.CommentLikesView.as_view(), name="comment-likes-list"),
]
