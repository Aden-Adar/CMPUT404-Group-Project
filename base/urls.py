from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("signup/", views.CreateAccount.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path("useless/", views.UselessView.as_view(), name="useless"),
]
