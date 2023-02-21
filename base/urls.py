from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("signup/", views.CreateAccount.as_view(), name="signup"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]
