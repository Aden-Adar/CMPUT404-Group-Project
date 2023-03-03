from django.urls import path
from . import views


urlpatterns = [
    path("authors/<uuid:id>/",views.SingleAuthorView.as_view(), name="author-detail"),
    path("authors/",views.AllAuthorView.as_view(), name="author-list")
]
