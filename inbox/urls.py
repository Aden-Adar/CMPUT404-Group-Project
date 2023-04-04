from django.urls import path
from . import views

'''
Contains the URLs for the authors endpoints.

Preceding URL is /service/authors/{author_id}/inbox/ 
'''

urlpatterns = [
    path("",views.InboxView, name="inbox-list"),
]