from django.urls import path
from . import views


urlpatterns = [
    path("",views.InboxView, name="inbox-list"),
]