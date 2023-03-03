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

def render_react(request):
    return render(request, "index.html")

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include("django.contrib.auth.urls")),

    path('service/', include("base.urls")),
    path('service/authors/', include("authors.urls")),
    path('service/posts/', include("posts.urls")),
    path('service/posts/<uuid:post_id>/', include("comments.urls")),
    path('service/posts/<uuid:post_id>/', include("likes.urls")),
    path('service/imgupload/', include("images.urls")),

    re_path(r"^$", render_react),
    re_path(r"^(?:.*)/?$", render_react),
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
