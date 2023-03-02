from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path("signup/", views.CreateAccount.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path("useless/", views.UselessView.as_view(), name="useless"),
    path("posts/", views.PostView.as_view(), name="posts-list"),
    path("posts/<uuid:post_id>/", views.PostView.as_view(), name="post-detail"),
    path("posts/<uuid:post_id>/comments/",views.CommentView.as_view(), name="comments-list"),
    path("posts/<uuid:post_id>/comments/<uuid:comment_id>/",views.CommentView.as_view(), name="comment-detail"),

    path('posts/<uuid:post_id>/likes/', views.PostLikesView.as_view(), name="post-likes-list"),
    path('posts/<uuid:post_id>/comments/<uuid:comment_id>/likes/', views.CommentLikesView.as_view(), name="comment-likes-list"),

    path("imgupload/",views.ImageView.as_view()),
    path("authors/<uuid:id>/",views.SingleAuthorView.as_view(), name="author-detail"),
    path("authors/",views.AllAuthorView.as_view(), name="author-list")
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
