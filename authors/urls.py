from django.urls import path
from . import views


urlpatterns = [
    path("<uuid:id>/",views.SingleAuthorView.as_view(), name="author-detail"),
    path("",views.AllAuthorView.as_view(), name="author-list")
]
