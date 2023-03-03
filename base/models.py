# from django.db import models
# from django.contrib.auth.models import AbstractUser, PermissionsMixin
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# import uuid

# from rest_framework.authtoken.models import Token
# from .manager import CustomUserManager
# # Create your models here.





# '''
# -- Followers
# Description: Followers of a user
# PRIMARY KEY: indexes
# FOREIGN KEYS: author_id

# class Followers(models.Model):
#     author_id = models.ForeignKey(CustomUser,null=True, on_delete=models.CASCADE,related_name='author')
#     follower_id = models.ForeignKey(CustomUser,null=True, on_delete=models.CASCADE,related_name='follower')
#     indexes = [
#         models.Index(fields=['author_id','follower_id'])
#     ]
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)

# '''


