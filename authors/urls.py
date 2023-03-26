from django.urls import path
from . import views


urlpatterns = [
    path("authors/<uuid:id>/",views.SingleAuthorView.as_view(), name="author-detail"),
    path("authors/",views.AllAuthorView.as_view(), name="author-list"),
    path("authors/<uuid:id>/followers/",views.FollowerList.as_view(), name="author-followers"),
    path("authors/<uuid:id>/followers/<uuid:follow_id>/", views.FollowingView.as_view(), name="single-author-followers"),
]
