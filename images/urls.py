from django.urls import path
from . import views


urlpatterns = [
    path("imgupload/",views.ImageView.as_view()),
]
