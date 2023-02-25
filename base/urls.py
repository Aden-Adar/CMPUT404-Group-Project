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
    path("posts/", views.PostMixinView.as_view()),
    path("posts/<int:pk>/", views.PostMixinView.as_view()),
    path("posts/<int:pk>/comments/",views.CommentView.as_view()),
    path("posts/<int:pk>/comments/<int:id>/",views.CommentView.as_view()),
    path("imgupload/",views.ImageView.as_view())
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT_IMAGE)
