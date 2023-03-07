"""socialdistribution URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import render
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
    title="Socialdistribution API",
    default_version='v1',
    #   description="Test description",
    #   terms_of_service="https://www.google.com/policies/terms/",
    #   contact=openapi.Contact(email="contact@snippets.local"),
    license=openapi.License(name="Apache License 2.0"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

def render_react(request):
    return render(request, "index.html")

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include("django.contrib.auth.urls")),

    path('service/', include("base.urls")),

    path('service/', include("authors.urls"), name='authors'),

    path('service/authors/<uuid:author_id>/posts/', include("posts.urls"), name='posts'),

    path('service/authors/<uuid:author_id>/posts/<uuid:post_id>/comments/', include("comments.urls"), name='comments'),

    path('service/authors/<uuid:author_id>/', include("likes.urls"), name='likes'),

    path('service/authors/<uuid:author_id>/inbox/', include('inbox.urls')),

    path('service/imgupload/', include("images.urls")),

    

    re_path('service/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    re_path(r"^$", render_react),
    #re_path(r"^(?:.*)/?$", render_react),
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
