from django.urls import path
from . import views


urlpatterns = [
    path("",views.ImageView.as_view()),
]
